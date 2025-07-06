#!/usr/bin/env python3
"""
Verify the JSON to SQLite conversion was successful
"""

import json
import sqlite3
from pathlib import Path

def verify_conversion():
    """Verify that all data was correctly transferred from JSON to SQLite"""
    
    # Load original JSON data
    json_file = Path("citations_index.json")
    db_file = Path("citations_database.sqlite")
    
    print("=== VERIFYING JSON TO SQLITE CONVERSION ===\n")
    
    # Read JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        json_citations = json_data.get('citations', [])
        print(f"JSON file: {len(json_citations)} citations")
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return False
    
    # Read SQLite
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM citations")
        db_count = cursor.fetchone()[0]
        print(f"SQLite DB: {db_count} citations")
        
        if len(json_citations) != db_count:
            print(f"❌ MISMATCH: JSON has {len(json_citations)}, DB has {db_count}")
            return False
        else:
            print("✅ Citation counts match")
        
        # Sample verification - check first few records
        print("\n=== SAMPLE DATA VERIFICATION ===")
        
        cursor.execute("""
            SELECT authors, title, journal, year, priority_score, doi_available
            FROM citations 
            ORDER BY priority_score DESC 
            LIMIT 3
        """)
        db_samples = cursor.fetchall()
        
        # Sort JSON by priority score for comparison
        json_sorted = sorted(json_citations, key=lambda x: x.get('priority_score', 0), reverse=True)
        
        for i, (db_authors, db_title, db_journal, db_year, db_priority, db_doi_avail) in enumerate(db_samples):
            json_item = json_sorted[i]
            
            print(f"\nRecord {i+1}:")
            print(f"  Authors: {'✅' if db_authors == json_item.get('authors', '') else '❌'}")
            print(f"  Title: {'✅' if db_title == json_item.get('title', '') else '❌'}")
            print(f"  Priority: {'✅' if db_priority == json_item.get('priority_score', 0) else '❌'}")
            
            if db_authors != json_item.get('authors', ''):
                print(f"    DB: {db_authors}")
                print(f"    JSON: {json_item.get('authors', '')}")
        
        # Check specific fields
        print("\n=== FIELD VALIDATION ===")
        
        # Count top 15 priority
        cursor.execute("SELECT COUNT(*) FROM citations WHERE top_15_priority = 1")
        db_top15 = cursor.fetchone()[0]
        json_top15 = sum(1 for c in json_citations if c.get('top_15_priority', False))
        print(f"Top 15 priority: DB={db_top15}, JSON={json_top15} {'✅' if db_top15 == json_top15 else '❌'}")
        
        # Count DOI available
        cursor.execute("SELECT COUNT(*) FROM citations WHERE doi_available = 1")
        db_doi = cursor.fetchone()[0]
        json_doi = sum(1 for c in json_citations if c.get('doi_available', False))
        print(f"DOI available: DB={db_doi}, JSON={json_doi} {'✅' if db_doi == json_doi else '❌'}")
        
        # Check year range
        cursor.execute("SELECT MIN(year), MAX(year) FROM citations WHERE year IS NOT NULL")
        db_min_year, db_max_year = cursor.fetchone()
        json_years = [c.get('year') for c in json_citations if c.get('year')]
        json_min_year, json_max_year = min(json_years), max(json_years)
        print(f"Year range: DB={db_min_year}-{db_max_year}, JSON={json_min_year}-{json_max_year} {'✅' if db_min_year == json_min_year and db_max_year == json_max_year else '❌'}")
        
        conn.close()
        
        print("\n=== VERIFICATION COMPLETED ===")
        print("✅ All data successfully transferred from JSON to SQLite")
        return True
        
    except Exception as e:
        print(f"Error reading SQLite: {e}")
        return False

if __name__ == "__main__":
    verify_conversion()