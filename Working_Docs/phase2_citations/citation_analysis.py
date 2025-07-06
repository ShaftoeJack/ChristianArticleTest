#!/usr/bin/env python3
"""
Citation frequency analysis and priority scoring for dicynodont paleontology paper
"""

import json
import re
from collections import defaultdict
from typing import Dict, List, Tuple, Set

def load_citations_index(filepath: str) -> Dict:
    """Load the citations index JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_citations_index(filepath: str, data: Dict) -> None:
    """Save the enhanced citations index JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_citation_patterns(text: str) -> List[str]:
    """Extract all citation patterns from text"""
    # Pattern to match standard academic citations
    pattern = r'\b[A-Z][a-z]+\s+(?:et al\.|&\s+[A-Z][a-z]+),?\s+\d{4}[a-z]?\b'
    return re.findall(pattern, text)

def normalize_citation(citation: str) -> str:
    """Normalize citation format for matching"""
    # Remove extra spaces and standardize format
    citation = re.sub(r'\s+', ' ', citation.strip())
    # Remove comma before year if present
    citation = re.sub(r',\s+(\d{4})', r' \1', citation)
    return citation

def match_citation_to_index(citation: str, citations_data: List[Dict]) -> int:
    """Match a citation pattern to a citation in the index"""
    normalized = normalize_citation(citation)
    
    for idx, entry in enumerate(citations_data):
        authors = entry.get('authors', '')
        year = entry.get('year', '')
        
        # Create possible patterns from the indexed citation
        if ' & ' in authors:
            # Two authors
            author_parts = authors.split(' & ')
            if len(author_parts) == 2:
                first_author = author_parts[0].split()[-1]  # Last name
                second_author = author_parts[1].split()[-1]  # Last name
                pattern1 = f"{first_author} & {second_author} {year}"
                pattern2 = f"{first_author} & {second_author}, {year}"
                if normalized in [pattern1, pattern2]:
                    return idx
        
        # Multiple authors (et al.)
        first_author = authors.split()[0] if authors else ''
        pattern1 = f"{first_author} et al. {year}"
        pattern2 = f"{first_author} et al., {year}"
        if normalized in [pattern1, pattern2]:
            return idx
    
    return -1

def analyze_citations():
    """Main analysis function"""
    # Load data
    citations_data = load_citations_index('Working_Docs/phase2_citations/citations_index.json')
    
    # Read article text
    with open('Working_Docs/phase1_ingestion/article_text.txt', 'r', encoding='utf-8') as f:
        article_text = f.read()
    
    # Read introduction citations
    with open('Working_Docs/phase2_citations/introduction_citations.txt', 'r', encoding='utf-8') as f:
        intro_citations = [line.strip() for line in f.readlines() if line.strip()]
    
    # Read citation frequency data
    citation_frequencies = {}
    with open('Working_Docs/phase2_citations/citation_frequency_analysis.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(None, 1)
                if len(parts) == 2:
                    count = int(parts[0])
                    citation = parts[1]
                    citation_frequencies[normalize_citation(citation)] = count
    
    # Track introduction citations
    intro_set = set()
    for citation in intro_citations:
        intro_set.add(normalize_citation(citation))
    
    # Process each citation in the index
    enhanced_citations = []
    for citation_entry in citations_data['citations']:
        authors = citation_entry.get('authors', '')
        year = citation_entry.get('year', '')
        
        # Generate possible citation patterns
        possible_patterns = []
        if ' & ' in authors:
            # Two authors
            author_parts = authors.split(' & ')
            if len(author_parts) == 2:
                first_author = author_parts[0].split()[-1]
                second_author = author_parts[1].split()[-1]
                possible_patterns.extend([
                    f"{first_author} & {second_author} {year}",
                    f"{first_author} & {second_author}, {year}"
                ])
        
        # Multiple authors (et al.)
        first_author = authors.split()[0] if authors else ''
        possible_patterns.extend([
            f"{first_author} et al. {year}",
            f"{first_author} et al., {year}"
        ])
        
        # Find frequency
        main_text_frequency = 0
        for pattern in possible_patterns:
            normalized = normalize_citation(pattern)
            if normalized in citation_frequencies:
                main_text_frequency = citation_frequencies[normalized]
                break
        
        # Check if in introduction
        introduction_mention = False
        for pattern in possible_patterns:
            if normalize_citation(pattern) in intro_set:
                introduction_mention = True
                break
        
        # Check if recent (2018-2023)
        recent_publication = year >= 2018 if year else False
        
        # Check if DOI available
        doi_available = citation_entry.get('doi') is not None
        
        # Calculate priority score
        priority_score = 0
        if introduction_mention:
            priority_score += 3
        priority_score += main_text_frequency
        if recent_publication:
            priority_score += 1
        if doi_available:
            priority_score += 1
        
        # Categorize citation based on content
        title = citation_entry.get('title', '').lower()
        journal = citation_entry.get('journal', '').lower()
        
        category = 'foundational'  # default
        if any(term in title for term in ['method', 'technique', 'analysis', 'ct', 'scan', 'microscopy']):
            category = 'methodological'
        elif any(term in title for term in ['phylogen', 'comparison', 'similar', 'related']):
            category = 'comparative'
        elif year and year >= 2018:
            category = 'recent_developments'
        elif any(term in title for term in ['framework', 'theory', 'concept', 'model']):
            category = 'theoretical'
        
        # Create enhanced entry
        enhanced_entry = citation_entry.copy()
        enhanced_entry.update({
            'priority_score': priority_score,
            'introduction_mention': introduction_mention,
            'main_text_frequency': main_text_frequency,
            'recent_publication': recent_publication,
            'doi_available': doi_available,
            'category': category
        })
        
        enhanced_citations.append(enhanced_entry)
    
    # Sort by priority score to identify top 15
    enhanced_citations.sort(key=lambda x: x['priority_score'], reverse=True)
    
    # Mark top 15
    for i in range(len(enhanced_citations)):
        enhanced_citations[i]['top_15_priority'] = i < 15
    
    # Save enhanced data
    enhanced_data = {'citations': enhanced_citations}
    save_citations_index('Working_Docs/phase2_citations/citations_index.json', enhanced_data)
    
    # Generate summary report
    generate_summary_report(enhanced_citations)
    
    print("Citation analysis complete!")
    print(f"Analyzed {len(enhanced_citations)} citations")
    print(f"Found {len([c for c in enhanced_citations if c['main_text_frequency'] > 0])} citations with main text mentions")
    print(f"Found {len([c for c in enhanced_citations if c['introduction_mention']])} citations in introduction")

def generate_summary_report(citations: List[Dict]) -> None:
    """Generate a summary report of the citation analysis"""
    
    # Sort by priority score
    top_citations = sorted(citations, key=lambda x: x['priority_score'], reverse=True)[:15]
    
    # Category counts
    category_counts = defaultdict(int)
    for citation in citations:
        category_counts[citation['category']] += 1
    
    # Introduction citations
    intro_citations = [c for c in citations if c['introduction_mention']]
    
    report = f"""# Citation Priority Analysis Report

## Summary Statistics

- **Total Citations Analyzed**: {len(citations)}
- **Citations with Main Text Mentions**: {len([c for c in citations if c['main_text_frequency'] > 0])}
- **Citations in Introduction**: {len(intro_citations)}
- **Recent Publications (2018-2023)**: {len([c for c in citations if c['recent_publication']])}
- **Citations with DOI**: {len([c for c in citations if c['doi_available']])}

## Top 15 Highest Priority Citations

| Rank | Authors | Year | Priority Score | Category | Main Text Frequency | Introduction | DOI |
|------|---------|------|----------------|----------|-------------------|-------------|-----|
"""
    
    for i, citation in enumerate(top_citations, 1):
        doi_status = "✓" if citation['doi_available'] else "✗"
        intro_status = "✓" if citation['introduction_mention'] else "✗"
        
        report += f"| {i} | {citation['authors']} | {citation['year']} | {citation['priority_score']} | {citation['category']} | {citation['main_text_frequency']} | {intro_status} | {doi_status} |\n"
    
    report += f"""

## Citation Category Breakdown

"""
    
    for category, count in sorted(category_counts.items()):
        percentage = (count / len(citations)) * 100
        report += f"- **{category.replace('_', ' ').title()}**: {count} citations ({percentage:.1f}%)\n"
    
    report += f"""

## Citation Frequency Analysis

### Most Frequently Cited Sources (Top 20)

"""
    
    frequent_citations = sorted(
        [c for c in citations if c['main_text_frequency'] > 0],
        key=lambda x: x['main_text_frequency'],
        reverse=True
    )[:20]
    
    for i, citation in enumerate(frequent_citations, 1):
        report += f"{i}. {citation['authors']} ({citation['year']}) - {citation['main_text_frequency']} mentions\n"
    
    report += f"""

### Introduction Citations (Foundation References)

"""
    
    for citation in sorted(intro_citations, key=lambda x: x['priority_score'], reverse=True):
        report += f"- {citation['authors']} ({citation['year']}) - Priority Score: {citation['priority_score']}\n"
    
    report += f"""

## Strategic Collection Recommendations

### Immediate Priority (Top 5)
These citations have the highest priority scores and should be collected first:

"""
    
    for i, citation in enumerate(top_citations[:5], 1):
        title = citation.get('title', 'N/A')
        journal = citation.get('journal', 'N/A')
        report += f"{i}. **{citation['authors']} ({citation['year']})**\n"
        report += f"   - Title: {title}\n"
        report += f"   - Journal: {journal}\n"
        report += f"   - Priority Score: {citation['priority_score']}\n"
        report += f"   - Main Text Frequency: {citation['main_text_frequency']}\n"
        report += f"   - Category: {citation['category']}\n\n"
    
    report += f"""

### High Priority (Ranks 6-15)
These citations should be collected as a second priority:

"""
    
    for i, citation in enumerate(top_citations[5:15], 6):
        report += f"{i}. {citation['authors']} ({citation['year']}) - Score: {citation['priority_score']}\n"
    
    report += f"""

### Category-Based Collection Strategy

1. **Foundational References**: Focus on highly cited foundational work that establishes basic principles
2. **Methodological Papers**: Collect papers describing key techniques and analytical methods
3. **Comparative Studies**: Gather papers that provide comparative context and similar research
4. **Recent Developments**: Prioritize recent publications that represent current state of knowledge
5. **Theoretical Frameworks**: Include papers that provide conceptual frameworks

### Notes on Citation Availability

- {len([c for c in citations if c['doi_available']])} citations have DOI information for easier access
- {len([c for c in citations if not c['doi_available']])} citations may require additional search effort
- Introduction citations are particularly important as they establish the theoretical foundation

## Next Steps

1. Begin with the top 5 immediate priority citations
2. Systematically work through the high priority list (ranks 6-15)
3. Use category-based strategy to ensure comprehensive coverage
4. Document any citations that cannot be obtained for alternative sourcing strategies
"""
    
    # Save report
    with open('Working_Docs/phase2_citations/priority_analysis.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("Summary report generated: Working_Docs/phase2_citations/priority_analysis.md")

if __name__ == "__main__":
    analyze_citations()