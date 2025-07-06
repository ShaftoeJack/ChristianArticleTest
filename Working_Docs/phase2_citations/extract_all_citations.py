#!/usr/bin/env python3
"""
Citation Extraction Script
Extracts ALL citations from the article text and creates a comprehensive citations_index.json
"""

import re
import json
from typing import List, Dict, Optional
import argparse

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
    
    # Split into individual citation blocks
    # Citations typically start with an author name followed by year
    citation_patterns = [
        # Pattern 1: Author et al. YEAR. — Title
        r'^([A-Z][a-zA-Z\s,&\.]+?)(\d{4}[a-z]?)\.\s*—\s*(.+?)(?=^\w|\Z)',
        # Pattern 2: Author YEAR. — Title
        r'^([A-Z][a-zA-Z\s,&\.]+?)(\d{4}[a-z]?)\.\s*—\s*(.+?)(?=^\w|\Z)',
        # Pattern 3: Author (YEAR) Title
        r'^([A-Z][a-zA-Z\s,&\.]+?)\s*\((\d{4}[a-z]?)\)\s*[\.—]\s*(.+?)(?=^\w|\Z)'
    ]
    
    # Process line by line to capture complete citations
    lines = references_text.split('\n')
    current_citation = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Remove line numbers if present (format: digits→)
        line = re.sub(r'^\d+→', '', line)
        
        # Check if this line starts a new citation (begins with capital letter and contains year)
        if re.match(r'^[A-Z][a-zA-Z\s,&\.]+?\s+\d{4}[a-z]?\.', line):
            # Process previous citation if exists
            if current_citation.strip():
                citation = parse_citation(current_citation.strip(), citation_id)
                if citation:
                    citations.append(citation)
                    citation_id += 1
            
            # Start new citation
            current_citation = line
        else:
            # Continue current citation
            current_citation += " " + line
    
    # Process the last citation
    if current_citation.strip():
        citation = parse_citation(current_citation.strip(), citation_id)
        if citation:
            citations.append(citation)
    
    return citations

def parse_citation(citation_text: str, citation_id: int) -> Optional[Dict]:
    """Parse a single citation text into structured data."""
    
    # Clean up the citation text
    citation_text = re.sub(r'\s+', ' ', citation_text)
    
    # Try different patterns to extract components
    patterns = [
        # Pattern 1: Author(s) Year. — Title. Journal Volume (Issue): Pages. DOI/URL
        r'^(.+?)\s+(\d{4}[a-z]?)\.\s*—\s*(.+?)\.\s*(.+?)\s+(\d+)(?:\s*\((\d+)\))?\s*:\s*([0-9\-]+)\.\s*(https?://.+|doi:.+)?',
        
        # Pattern 2: Author(s) Year. — Title. Journal Volume: Pages. DOI/URL
        r'^(.+?)\s+(\d{4}[a-z]?)\.\s*—\s*(.+?)\.\s*(.+?)\s+(\d+)\s*:\s*([0-9\-]+)\.\s*(https?://.+|doi:.+)?',
        
        # Pattern 3: Author(s) Year. — Title. Publisher/Location info
        r'^(.+?)\s+(\d{4}[a-z]?)\.\s*—\s*(.+?)\.\s*(.+)',
        
        # Pattern 4: Simplified - Author(s) Year. Title info
        r'^(.+?)\s+(\d{4}[a-z]?)\.\s*(.+)'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, citation_text, re.DOTALL)
        if match:
            groups = match.groups()
            
            # Basic extraction
            authors = clean_authors(groups[0])
            year = int(groups[1][:4])  # Extract just the year number
            
            # Handle different pattern matches
            if len(groups) >= 3:
                title = clean_title(groups[2])
            else:
                title = "Title not parsed"
            
            if len(groups) >= 4:
                publication_info = groups[3]
            else:
                publication_info = ""
            
            # Extract journal, volume, issue, pages, DOI
            journal, volume, issue, pages, doi, url = extract_publication_details(publication_info, citation_text)
            
            return {
                "id": citation_id,
                "authors": authors,
                "title": title,
                "journal": journal,
                "year": year,
                "volume": volume,
                "issue": issue,
                "pages": pages,
                "doi": doi,
                "url": url,
                "raw_text": citation_text[:200] + "..." if len(citation_text) > 200 else citation_text
            }
    
    # If no pattern matches, create a basic entry
    year_match = re.search(r'\b(\d{4})[a-z]?\b', citation_text)
    year = int(year_match.group(1)) if year_match else None
    
    return {
        "id": citation_id,
        "authors": extract_first_author(citation_text),
        "title": "Title extraction failed",
        "journal": "Journal not identified",
        "year": year,
        "volume": "",
        "issue": "",
        "pages": "",
        "doi": "",
        "url": "",
        "raw_text": citation_text[:200] + "..." if len(citation_text) > 200 else citation_text
    }

def clean_authors(author_text: str) -> str:
    """Clean and format author names."""
    # Remove trailing periods and extra spaces
    author_text = re.sub(r'\.$', '', author_text.strip())
    # Handle common patterns
    author_text = re.sub(r'\s+', ' ', author_text)
    return author_text

def clean_title(title_text: str) -> str:
    """Clean and format title text."""
    # Remove trailing periods and clean up
    title_text = re.sub(r'\.$', '', title_text.strip())
    title_text = re.sub(r'\s+', ' ', title_text)
    return title_text

def extract_first_author(text: str) -> str:
    """Extract the first author from citation text."""
    # Look for pattern like "LastName F." or "LastName, F."
    match = re.match(r'^([A-Z][a-zA-Z]+(?:\s+[A-Z]\.)*)', text)
    if match:
        return match.group(1)
    return "Author not parsed"

def extract_publication_details(pub_info: str, full_text: str) -> tuple:
    """Extract journal, volume, issue, pages, DOI, and URL from publication info."""
    journal = ""
    volume = ""
    issue = ""
    pages = ""
    doi = ""
    url = ""
    
    # Extract URL
    url_match = re.search(r'(https?://[^\s]+)', full_text)
    if url_match:
        url = url_match.group(1)
    
    # Extract DOI
    doi_match = re.search(r'(?:doi:|https://doi\.org/)([^\s]+)', full_text)
    if doi_match:
        doi = doi_match.group(1)
    
    # Extract volume, issue, pages pattern: Volume (Issue): Pages
    vol_match = re.search(r'(\w+(?:\s+\w+)*)\s+(\d+)(?:\s*\((\d+)\))?\s*:\s*([0-9\-]+)', pub_info)
    if vol_match:
        journal = vol_match.group(1).strip()
        volume = vol_match.group(2)
        issue = vol_match.group(3) or ""
        pages = vol_match.group(4)
    else:
        # Try to extract journal name from beginning of pub_info
        journal_match = re.match(r'^([^0-9]+?)(?:\s+\d+|$)', pub_info)
        if journal_match:
            journal = journal_match.group(1).strip()
    
    return journal, volume, issue, pages, doi, url

def analyze_citations(citations: List[Dict]) -> Dict:
    """Analyze the extracted citations and provide statistics."""
    if not citations:
        return {}
    
    years = [c['year'] for c in citations if c['year']]
    journals = [c['journal'] for c in citations if c['journal'] and c['journal'] != "Journal not identified"]
    
    # Count journal frequency
    journal_counts = {}
    for journal in journals:
        journal_counts[journal] = journal_counts.get(journal, 0) + 1
    
    # Get most common journals
    most_common_journals = sorted(journal_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    analysis = {
        "total_citations": len(citations),
        "year_range": f"{min(years)}-{max(years)}" if years else "Unknown",
        "most_common_journals": most_common_journals,
        "unique_journals": len(set(journals)),
        "citations_with_dois": len([c for c in citations if c['doi']]),
        "citations_with_urls": len([c for c in citations if c['url']]),
    }
    
    return analysis

def main():
    parser = argparse.ArgumentParser(description='Extract citations from article text')
    parser.add_argument('--input', default='/Users/jrlynn/Projects/GIT_Repos/ChristianArticleTest/Working_Docs/phase1_ingestion/article_text.txt',
                        help='Input article text file')
    parser.add_argument('--output', default='/Users/jrlynn/Projects/GIT_Repos/ChristianArticleTest/Working_Docs/phase2_citations/citations_index.json',
                        help='Output citations JSON file')
    
    args = parser.parse_args()
    
    # Read the article text
    print(f"Reading article text from: {args.input}")
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract citations
    print("Extracting citations...")
    citations = extract_citations_from_text(text)
    
    # Analyze citations
    analysis = analyze_citations(citations)
    
    # Create output structure
    output_data = {
        "metadata": {
            "extraction_date": "2025-01-05",
            "source_file": args.input,
            "extraction_method": "Comprehensive regex-based parsing",
            "total_citations": len(citations)
        },
        "analysis": analysis,
        "citations": citations
    }
    
    # Save to JSON file
    print(f"Saving {len(citations)} citations to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n=== CITATION EXTRACTION SUMMARY ===")
    print(f"Total citations extracted: {len(citations)}")
    if analysis:
        print(f"Year range: {analysis.get('year_range', 'Unknown')}")
        print(f"Unique journals: {analysis.get('unique_journals', 0)}")
        print(f"Citations with DOIs: {analysis.get('citations_with_dois', 0)}")
        print(f"Citations with URLs: {analysis.get('citations_with_urls', 0)}")
        
        print(f"\nMost common journals:")
        for journal, count in analysis.get('most_common_journals', [])[:5]:
            print(f"  {journal}: {count} citations")
    
    print(f"\nComplete database saved to: {args.output}")

if __name__ == "__main__":
    main()