#!/usr/bin/env python3
"""
Comprehensive Citation Frequency Analysis Script
Analyzes all 578 citations for frequency mentions and priority scoring
"""

import json
import re
import os
from collections import defaultdict
from datetime import datetime

def load_citations_database(file_path):
    """Load the complete citations database"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_article_text(file_path):
    """Load the article text"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_introduction_section(file_path):
    """Load the introduction section"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_citation_patterns(text):
    """Extract all citation patterns from text"""
    # Common citation patterns
    patterns = [
        r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+et\s+al\.\s*[,\s]*(\d{4}[a-z]?)',
        r'\b([A-Z][a-zA-Z]+(?:\s+&\s+[A-Z][a-zA-Z]+)*)\s*[,\s]*(\d{4}[a-z]?)',
        r'\b([A-Z][a-zA-Z]+)\s*[,\s]*(\d{4}[a-z]?)',
        r'\(([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+et\s+al\.\s*[,\s]*(\d{4}[a-z]?)\)',
        r'\(([A-Z][a-zA-Z]+(?:\s+&\s+[A-Z][a-zA-Z]+)*)\s*[,\s]*(\d{4}[a-z]?)\)',
        r'\(([A-Z][a-zA-Z]+)\s*[,\s]*(\d{4}[a-z]?)\)'
    ]
    
    citations_found = []
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) == 2:
                author, year = match
                citations_found.append((author.strip(), year.strip()))
    
    return citations_found

def match_citation_to_database(citation_tuple, citations_list):
    """Match a citation pattern to database entries"""
    author, year = citation_tuple
    matches = []
    
    for citation_data in citations_list:
        if not isinstance(citation_data, dict):
            continue
            
        db_authors = citation_data.get('authors', '').lower()
        db_year = str(citation_data.get('year', ''))
        citation_id = citation_data.get('id', '')
        
        # Check if the author matches (fuzzy matching)
        if author.lower() in db_authors or any(part.lower() in db_authors for part in author.split()):
            if year in db_year:
                matches.append(citation_id)
    
    return matches

def calculate_priority_score(citation_data, intro_mentions, main_mentions):
    """Calculate priority score for a citation"""
    score = 0
    
    # Introduction mention (+3)
    if intro_mentions > 0:
        score += 3
    
    # Main text mentions (+1 each)
    score += main_mentions
    
    # Recent publication 2018-2023 (+1)
    year = citation_data.get('year', 0)
    if isinstance(year, (int, str)) and str(year).isdigit():
        if 2018 <= int(year) <= 2023:
            score += 1
    
    # DOI available (+1)
    if citation_data.get('doi'):
        score += 1
    
    return score

def main():
    # File paths
    base_dir = "/Users/jrlynn/Projects/GIT_Repos/ChristianArticleTest/Working_Docs"
    citations_file = os.path.join(base_dir, "phase2_citations", "citations_index.json")
    article_file = os.path.join(base_dir, "phase1_ingestion", "article_text.txt")
    intro_file = os.path.join(base_dir, "phase1_ingestion", "introduction_section.txt")
    
    # Load data
    print("Loading citations database...")
    citations_db = load_citations_database(citations_file)
    
    print("Loading article text...")
    article_text = load_article_text(article_file)
    
    print("Loading introduction section...")
    intro_text = load_introduction_section(intro_file)
    
    # Extract citation patterns
    print("Extracting citation patterns from main text...")
    main_text_citations = extract_citation_patterns(article_text)
    
    print("Extracting citation patterns from introduction...")
    intro_citations = extract_citation_patterns(intro_text)
    
    # Count frequencies
    print("Matching citations to database...")
    citation_frequencies = defaultdict(int)
    intro_frequencies = defaultdict(int)
    
    # Get citations list from database
    citations_list = citations_db.get('citations', [])
    
    # Process main text citations
    for citation_tuple in main_text_citations:
        matches = match_citation_to_database(citation_tuple, citations_list)
        for match in matches:
            citation_frequencies[match] += 1
    
    # Process introduction citations
    for citation_tuple in intro_citations:
        matches = match_citation_to_database(citation_tuple, citations_list)
        for match in matches:
            intro_frequencies[match] += 1
    
    # Update citations database with priority data
    print("Calculating priority scores...")
    updated_citations_list = []
    priority_list = []
    
    for citation_data in citations_list:
        if not isinstance(citation_data, dict):
            continue
            
        citation_id = citation_data.get('id', '')
        main_freq = citation_frequencies.get(citation_id, 0)
        intro_freq = intro_frequencies.get(citation_id, 0)
        
        # Calculate priority score
        priority_score = calculate_priority_score(citation_data, intro_freq, main_freq)
        
        # Update citation data
        updated_citation = citation_data.copy()
        updated_citation['priority_score'] = priority_score
        updated_citation['introduction_mention'] = intro_freq > 0
        updated_citation['main_text_frequency'] = main_freq
        updated_citation['recent_publication'] = 2018 <= int(citation_data.get('year', 0)) <= 2023 if str(citation_data.get('year', '')).isdigit() else False
        updated_citation['doi_available'] = bool(citation_data.get('doi'))
        updated_citation['top_15_priority'] = False  # Initialize as False
        
        updated_citations_list.append(updated_citation)
        
        if priority_score > 0:  # Only include citations with mentions
            priority_list.append((citation_id, priority_score, citation_data))
    
    # Sort by priority score
    priority_list.sort(key=lambda x: x[1], reverse=True)
    
    # Mark top 15 priority citations
    for i, (citation_id, _, _) in enumerate(priority_list[:15]):
        for citation in updated_citations_list:
            if citation.get('id') == citation_id:
                citation['top_15_priority'] = True
                break
    
    # Rebuild the database structure
    updated_citations_db = {
        'metadata': citations_db.get('metadata', {}),
        'analysis': citations_db.get('analysis', {}),
        'citations': updated_citations_list
    }
    
    # Save updated citations database
    print("Saving updated citations database...")
    with open(citations_file, 'w', encoding='utf-8') as f:
        json.dump(updated_citations_db, f, indent=2, ensure_ascii=False)
    
    # Create analysis reports
    print("Creating analysis reports...")
    
    # Priority analysis report
    priority_report = []
    priority_report.append("# Citation Priority Analysis - Complete 578 Citation Database\n")
    priority_report.append(f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    priority_report.append(f"Total citations in database: {len(citations_list)}\n")
    priority_report.append(f"Citations with main text mentions: {len([k for k in citation_frequencies.keys()])}\n")
    priority_report.append(f"Citations with introduction mentions: {len([k for k in intro_frequencies.keys()])}\n\n")
    
    priority_report.append("## Top 15 Priority Citations\n")
    priority_report.append("Based on: Introduction mention (+3), main text mentions (+1 each), recent publication 2018-2023 (+1), DOI available (+1)\n\n")
    
    for i, (citation_id, priority_score, citation_data) in enumerate(priority_list[:15], 1):
        priority_report.append(f"### {i}. {citation_data.get('title', 'No title')}\n")
        priority_report.append(f"- **ID**: {citation_id}\n")
        priority_report.append(f"- **Authors**: {citation_data.get('authors', 'Unknown')}\n")
        priority_report.append(f"- **Year**: {citation_data.get('year', 'Unknown')}\n")
        priority_report.append(f"- **Journal**: {citation_data.get('journal', 'Unknown')}\n")
        priority_report.append(f"- **Priority Score**: {priority_score}\n")
        priority_report.append(f"- **Main Text Mentions**: {citation_frequencies.get(citation_id, 0)}\n")
        priority_report.append(f"- **Introduction Mention**: {'Yes' if intro_frequencies.get(citation_id, 0) > 0 else 'No'}\n")
        is_recent = str(citation_data.get('year', '')).isdigit() and 2018 <= int(citation_data.get('year', 0)) <= 2023
        priority_report.append(f"- **Recent Publication**: {'Yes' if is_recent else 'No'}\n")
        priority_report.append(f"- **DOI Available**: {'Yes' if citation_data.get('doi') else 'No'}\n\n")
    
    # Save priority analysis
    with open(os.path.join(base_dir, "phase2_citations", "priority_analysis.md"), 'w', encoding='utf-8') as f:
        f.write(''.join(priority_report))
    
    # Create frequency analysis report
    freq_report = []
    freq_report.append("# Citation Frequency Analysis - All Citations with Main Text Mentions\n")
    freq_report.append(f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # Sort by frequency
    sorted_frequencies = sorted(citation_frequencies.items(), key=lambda x: x[1], reverse=True)
    
    # Create lookup dictionary for citations
    citation_lookup = {citation.get('id'): citation for citation in citations_list}
    
    for citation_id, frequency in sorted_frequencies:
        citation_data = citation_lookup.get(citation_id, {})
        freq_report.append(f"**ID**: {citation_id} | **Frequency**: {frequency}\n")
        freq_report.append(f"**Authors**: {citation_data.get('authors', 'Unknown')}\n")
        freq_report.append(f"**Title**: {citation_data.get('title', 'No title')}\n")
        freq_report.append(f"**Year**: {citation_data.get('year', 'Unknown')}\n")
        freq_report.append(f"**Journal**: {citation_data.get('journal', 'Unknown')}\n\n")
    
    # Save frequency analysis
    with open(os.path.join(base_dir, "phase2_citations", "citation_frequency_analysis.txt"), 'w', encoding='utf-8') as f:
        f.write(''.join(freq_report))
    
    # Create introduction citations report
    intro_report = []
    intro_report.append("# Introduction Section Citations\n")
    intro_report.append(f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    for citation_id, frequency in intro_frequencies.items():
        citation_data = citation_lookup.get(citation_id, {})
        intro_report.append(f"**ID**: {citation_id} | **Mentions**: {frequency}\n")
        intro_report.append(f"**Authors**: {citation_data.get('authors', 'Unknown')}\n")
        intro_report.append(f"**Title**: {citation_data.get('title', 'No title')}\n")
        intro_report.append(f"**Year**: {citation_data.get('year', 'Unknown')}\n")
        intro_report.append(f"**Journal**: {citation_data.get('journal', 'Unknown')}\n\n")
    
    # Save introduction citations
    with open(os.path.join(base_dir, "phase2_citations", "introduction_citations.txt"), 'w', encoding='utf-8') as f:
        f.write(''.join(intro_report))
    
    print("Analysis complete!")
    print(f"Total citations analyzed: {len(citations_list)}")
    print(f"Citations with main text mentions: {len(citation_frequencies)}")
    print(f"Citations with introduction mentions: {len(intro_frequencies)}")
    print(f"Top priority score: {priority_list[0][1] if priority_list else 0}")

if __name__ == "__main__":
    main()