#!/usr/bin/env python3
"""
Improved Citation Extraction Script
Extracts ALL citations from the article text with better parsing
"""

import re
import json
from typing import List, Dict, Optional

def extract_citations_from_text(text: str) -> List[Dict]:
    """Extract citations from the references section of the text."""
    citations = []
    citation_id = 1
    
    # Find the references section
    references_match = re.search(r'REFERENCES\s*\n(.*)', text, re.DOTALL | re.IGNORECASE)
    if not references_match:
        print("No REFERENCES section found")
        return citations
    
    references_text = references_match.group(1)
    
    # Process line by line and look for citation patterns
    lines = references_text.split('\n')
    current_citation_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Remove line numbers if present (format: digits→)
        line = re.sub(r'^\d+→', '', line)
        line = line.strip()
        
        if not line:
            continue
        
        # Check if this line starts a new citation
        # Pattern: Author(s) followed by 4-digit year
        if re.match(r'^[A-Z][A-Za-z\s,&\.\-\']+?\s+\d{4}[a-z]?\.', line):
            # Process previous citation if exists
            if current_citation_lines:
                citation_text = ' '.join(current_citation_lines).strip()
                citation = parse_citation(citation_text, citation_id)
                if citation:
                    citations.append(citation)
                    citation_id += 1
            
            # Start new citation
            current_citation_lines = [line]
        else:
            # Continue current citation
            if current_citation_lines:  # Only add if we're in a citation
                current_citation_lines.append(line)
    
    # Process the last citation
    if current_citation_lines:
        citation_text = ' '.join(current_citation_lines).strip()
        citation = parse_citation(citation_text, citation_id)
        if citation:
            citations.append(citation)
    
    return citations

def parse_citation(citation_text: str, citation_id: int) -> Optional[Dict]:
    """Parse a single citation text into structured data."""
    
    # Clean up the citation text
    citation_text = re.sub(r'\s+', ' ', citation_text)
    
    # Extract basic components using regex patterns
    
    # Extract authors and year (beginning of citation)
    author_year_match = re.match(r'^(.+?)\s+(\d{4}[a-z]?)\.', citation_text)
    if not author_year_match:
        return None
    
    authors = author_year_match.group(1).strip()
    year_str = author_year_match.group(2)
    year = int(year_str[:4])  # Extract just the year number
    
    # Extract the rest after "author year."
    rest_text = citation_text[author_year_match.end():].strip()
    
    # Look for title (usually after " — ")
    title = ""
    if rest_text.startswith('—'):
        rest_text = rest_text[1:].strip()
        # Title is usually the first sentence/phrase
        title_match = re.match(r'^([^.]+)', rest_text)
        if title_match:
            title = title_match.group(1).strip()
            rest_text = rest_text[title_match.end():].strip()
            if rest_text.startswith('.'):
                rest_text = rest_text[1:].strip()
    
    # Extract DOI and URL
    doi = ""
    url = ""
    
    # Extract URL
    url_match = re.search(r'(https?://[^\s]+)', citation_text)
    if url_match:
        url = url_match.group(1)
    
    # Extract DOI
    doi_match = re.search(r'(?:doi:|https://doi\.org/)([^\s]+)', citation_text)
    if doi_match:
        doi = doi_match.group(1)
    
    # Extract journal and publication details
    journal, volume, issue, pages = extract_journal_info(rest_text)
    
    return {
        "id": citation_id,
        "authors": clean_authors(authors),
        "title": clean_title(title) if title else "Title not extracted",
        "journal": journal,
        "year": year,
        "volume": volume,
        "issue": issue,
        "pages": pages,
        "doi": doi,
        "url": url,
        "raw_text": citation_text[:300] + "..." if len(citation_text) > 300 else citation_text
    }

def extract_journal_info(text: str) -> tuple:
    """Extract journal, volume, issue, and pages from publication text."""
    journal = ""
    volume = ""
    issue = ""
    pages = ""
    
    # Common patterns:
    # Journal Volume (Issue): Pages
    # Journal Volume: Pages
    # Journal, Volume: Pages
    
    patterns = [
        # Pattern 1: Journal Volume (Issue): Pages
        r'^(.+?)\s+(\d+)\s*\((\d+)\)\s*:\s*([0-9\-]+)',
        # Pattern 2: Journal Volume: Pages
        r'^(.+?)\s+(\d+)\s*:\s*([0-9\-]+)',
        # Pattern 3: Journal, Volume: Pages
        r'^(.+?),?\s+(\d+)\s*:\s*([0-9\-]+)',
        # Pattern 4: Just journal name
        r'^([A-Za-z][^0-9]+?)(?:\s|$)',
    ]
    
    for i, pattern in enumerate(patterns):
        match = re.match(pattern, text)
        if match:
            groups = match.groups()
            journal = groups[0].strip()
            
            if len(groups) >= 2:
                volume = groups[1]
            if len(groups) >= 3:
                if i == 0:  # Pattern 1 has issue
                    issue = groups[2]
                    if len(groups) >= 4:
                        pages = groups[3]
                else:  # Pattern 2 and 3 have pages as group 3
                    pages = groups[2]
            break
    
    # Clean up journal name
    journal = re.sub(r'\.$', '', journal)
    journal = re.sub(r'\s+', ' ', journal)
    
    return journal, volume, issue, pages

def clean_authors(author_text: str) -> str:
    """Clean and format author names."""
    # Remove trailing periods and extra spaces
    author_text = re.sub(r'\.$', '', author_text.strip())
    # Handle common patterns and clean up spacing
    author_text = re.sub(r'\s+', ' ', author_text)
    return author_text

def clean_title(title_text: str) -> str:
    """Clean and format title text."""
    # Remove trailing periods and clean up
    title_text = re.sub(r'\.$', '', title_text.strip())
    title_text = re.sub(r'\s+', ' ', title_text)
    return title_text

def analyze_citations(citations: List[Dict]) -> Dict:
    """Analyze the extracted citations and provide statistics."""
    if not citations:
        return {}
    
    years = [c['year'] for c in citations if c['year']]
    journals = [c['journal'] for c in citations if c['journal'] and c['journal'].strip()]
    
    # Count journal frequency
    journal_counts = {}
    for journal in journals:
        if journal.strip():
            journal_counts[journal] = journal_counts.get(journal, 0) + 1
    
    # Get most common journals
    most_common_journals = sorted(journal_counts.items(), key=lambda x: x[1], reverse=True)[:15]
    
    analysis = {
        "total_citations": len(citations),
        "year_range": f"{min(years)}-{max(years)}" if years else "Unknown",
        "most_common_journals": most_common_journals,
        "unique_journals": len(set(j for j in journals if j.strip())),
        "citations_with_dois": len([c for c in citations if c['doi']]),
        "citations_with_urls": len([c for c in citations if c['url']]),
        "decades": get_decade_counts(years)
    }
    
    return analysis

def get_decade_counts(years: List[int]) -> Dict[str, int]:
    """Count citations by decade."""
    decade_counts = {}
    for year in years:
        decade = f"{(year // 10) * 10}s"
        decade_counts[decade] = decade_counts.get(decade, 0) + 1
    
    return dict(sorted(decade_counts.items()))

def main():
    input_file = '/Users/jrlynn/Projects/GIT_Repos/ChristianArticleTest/Working_Docs/phase1_ingestion/article_text.txt'
    output_file = '/Users/jrlynn/Projects/GIT_Repos/ChristianArticleTest/Working_Docs/phase2_citations/citations_index.json'
    
    # Read the article text
    print(f"Reading article text from: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract citations
    print("Extracting citations with improved parsing...")
    citations = extract_citations_from_text(text)
    
    # Analyze citations
    analysis = analyze_citations(citations)
    
    # Create output structure
    output_data = {
        "metadata": {
            "extraction_date": "2025-01-05",
            "source_file": input_file,
            "extraction_method": "Improved regex-based parsing with proper citation boundary detection",
            "total_citations": len(citations),
            "notes": "Complete extraction of all references from the scholarly article"
        },
        "analysis": analysis,
        "citations": citations
    }
    
    # Save to JSON file
    print(f"Saving {len(citations)} citations to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n=== COMPREHENSIVE CITATION EXTRACTION SUMMARY ===")
    print(f"Total citations extracted: {len(citations)}")
    if analysis:
        print(f"Year range: {analysis.get('year_range', 'Unknown')}")
        print(f"Unique journals: {analysis.get('unique_journals', 0)}")
        print(f"Citations with DOIs: {analysis.get('citations_with_dois', 0)}")
        print(f"Citations with URLs: {analysis.get('citations_with_urls', 0)}")
        
        print(f"\nMost common journals:")
        for journal, count in analysis.get('most_common_journals', [])[:10]:
            print(f"  {journal}: {count} citations")
        
        print(f"\nCitations by decade:")
        for decade, count in analysis.get('decades', {}).items():
            print(f"  {decade}: {count} citations")
    
    # Show sample citations
    print(f"\nSample parsed citations:")
    for i in range(min(3, len(citations))):
        cite = citations[i]
        print(f"\nCitation {cite['id']}:")
        print(f"  Authors: {cite['authors']}")
        print(f"  Year: {cite['year']}")
        print(f"  Title: {cite['title']}")
        print(f"  Journal: {cite['journal']}")
        if cite['volume']:
            print(f"  Volume: {cite['volume']}")
        if cite['pages']:
            print(f"  Pages: {cite['pages']}")
    
    print(f"\nComplete database saved to: {output_file}")

if __name__ == "__main__":
    main()