#!/usr/bin/env python3
"""
Convert citations_index.json to SQLite database for efficient context management.
"""

import json
import sqlite3
import os
from pathlib import Path

def create_citations_database():
    """Create SQLite database from citations_index.json"""
    
    # File paths
    json_file = Path("citations_index.json")
    db_file = Path("citations_database.sqlite")
    
    # Remove existing database if it exists
    if db_file.exists():
        db_file.unlink()
        print(f"Removed existing database: {db_file}")
    
    # Read JSON data
    print(f"Reading JSON file: {json_file}")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        citations = data.get('citations', [])
        print(f"Found {len(citations)} citations in JSON file")
        
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return False
    
    # Create SQLite database
    print(f"Creating SQLite database: {db_file}")
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Create table structure
        cursor.execute('''
            CREATE TABLE citations (
                id INTEGER PRIMARY KEY,
                authors TEXT,
                title TEXT,
                journal TEXT,
                year INTEGER,
                volume TEXT,
                issue TEXT,
                pages TEXT,
                doi TEXT,
                url TEXT,
                priority_score INTEGER,
                main_text_frequency INTEGER,
                introduction_mention BOOLEAN,
                recent_publication BOOLEAN,
                doi_available BOOLEAN,
                top_15_priority BOOLEAN,
                category TEXT
            )
        ''')
        
        # Create indexes for efficient queries
        cursor.execute('CREATE INDEX idx_priority_score ON citations(priority_score DESC)')
        cursor.execute('CREATE INDEX idx_top15 ON citations(top_15_priority)')
        cursor.execute('CREATE INDEX idx_year ON citations(year)')
        cursor.execute('CREATE INDEX idx_authors ON citations(authors)')
        cursor.execute('CREATE INDEX idx_doi ON citations(doi)')
        cursor.execute('CREATE INDEX idx_category ON citations(category)')
        
        print("Created table structure and indexes")
        
        # Insert citations data
        inserted_count = 0
        for citation in citations:
            try:
                cursor.execute('''
                    INSERT INTO citations (
                        authors, title, journal, year, volume, issue, pages, doi, url,
                        priority_score, main_text_frequency, introduction_mention,
                        recent_publication, doi_available, top_15_priority, category
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    citation.get('authors', ''),
                    citation.get('title', ''),
                    citation.get('journal', ''),
                    citation.get('year'),
                    citation.get('volume', ''),
                    citation.get('issue', ''),
                    citation.get('pages', ''),
                    citation.get('doi', ''),
                    citation.get('url', ''),
                    citation.get('priority_score', 0),
                    citation.get('main_text_frequency', 0),
                    citation.get('introduction_mention', False),
                    citation.get('recent_publication', False),
                    citation.get('doi_available', False),
                    citation.get('top_15_priority', False),
                    citation.get('category', '')
                ))
                inserted_count += 1
                
            except Exception as e:
                print(f"Error inserting citation: {e}")
                print(f"Citation data: {citation}")
                continue
        
        # Commit changes
        conn.commit()
        print(f"Successfully inserted {inserted_count} citations")
        
        # Verify data integrity
        cursor.execute('SELECT COUNT(*) FROM citations')
        total_count = cursor.fetchone()[0]
        print(f"Database contains {total_count} citations")
        
        # Test queries
        print("\nTesting database functionality:")
        
        # Test 1: Top 15 priority citations
        cursor.execute('SELECT COUNT(*) FROM citations WHERE top_15_priority = 1')
        top15_count = cursor.fetchone()[0]
        print(f"Top 15 priority citations: {top15_count}")
        
        # Test 2: Citations with DOIs
        cursor.execute('SELECT COUNT(*) FROM citations WHERE doi_available = 1')
        doi_count = cursor.fetchone()[0]
        print(f"Citations with DOIs: {doi_count}")
        
        # Test 3: Recent publications (2018-2023)
        cursor.execute('SELECT COUNT(*) FROM citations WHERE year >= 2018 AND year <= 2023')
        recent_count = cursor.fetchone()[0]
        print(f"Recent publications (2018-2023): {recent_count}")
        
        # Test 4: Categories
        cursor.execute('SELECT category, COUNT(*) FROM citations GROUP BY category')
        categories = cursor.fetchall()
        print(f"Categories: {categories}")
        
        conn.close()
        print(f"\nDatabase created successfully: {db_file}")
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == "__main__":
    print("Converting citations_index.json to SQLite database...")
    success = create_citations_database()
    if success:
        print("Conversion completed successfully!")
    else:
        print("Conversion failed!")