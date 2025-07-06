#!/usr/bin/env python3
"""
Test the SQLite citations database functionality
"""

import sqlite3
from pathlib import Path

def test_database():
    """Test various database queries"""
    
    db_file = Path("citations_database.sqlite")
    
    if not db_file.exists():
        print(f"Database file not found: {db_file}")
        return
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        print("=== DATABASE FUNCTIONALITY TESTS ===\n")
        
        # Test 1: Total citations
        cursor.execute("SELECT COUNT(*) FROM citations")
        total = cursor.fetchone()[0]
        print(f"1. Total citations: {total}")
        
        # Test 2: Top 5 priority citations
        cursor.execute("""
            SELECT authors, title, journal, year, priority_score 
            FROM citations 
            WHERE top_15_priority = 1 
            ORDER BY priority_score DESC 
            LIMIT 5
        """)
        top5 = cursor.fetchall()
        print(f"\n2. Top 5 Priority Citations:")
        for i, (authors, title, journal, year, score) in enumerate(top5, 1):
            print(f"   {i}. {authors} ({year}) - Priority: {score}")
            print(f"      Title: {title[:60]}...")
            print(f"      Journal: {journal}")
        
        # Test 3: Citations with DOIs
        cursor.execute("SELECT COUNT(*) FROM citations WHERE doi_available = 1")
        doi_count = cursor.fetchone()[0]
        print(f"\n3. Citations with DOIs: {doi_count}")
        
        # Test 4: Recent publications by year
        cursor.execute("""
            SELECT year, COUNT(*) as count 
            FROM citations 
            WHERE year >= 2018 AND year <= 2023 
            GROUP BY year 
            ORDER BY year DESC
        """)
        recent = cursor.fetchall()
        print(f"\n4. Recent Publications (2018-2023):")
        for year, count in recent:
            print(f"   {year}: {count} citations")
        
        # Test 5: Most cited journals
        cursor.execute("""
            SELECT journal, COUNT(*) as citation_count 
            FROM citations 
            WHERE journal != '' 
            GROUP BY journal 
            ORDER BY citation_count DESC 
            LIMIT 10
        """)
        journals = cursor.fetchall()
        print(f"\n5. Most Cited Journals:")
        for journal, count in journals:
            print(f"   {journal}: {count} citations")
        
        # Test 6: Priority score statistics
        cursor.execute("""
            SELECT 
                MIN(priority_score) as min_priority,
                MAX(priority_score) as max_priority,
                AVG(priority_score) as avg_priority,
                COUNT(*) as total_citations
            FROM citations
        """)
        stats = cursor.fetchone()
        print(f"\n6. Priority Score Statistics:")
        print(f"   Min: {stats[0]}, Max: {stats[1]}, Avg: {stats[2]:.2f}, Total: {stats[3]}")
        
        # Test 7: Data quality check
        cursor.execute("""
            SELECT 
                COUNT(*) as total_citations,
                COUNT(CASE WHEN authors != '' THEN 1 END) as has_authors,
                COUNT(CASE WHEN title != '' THEN 1 END) as has_title,
                COUNT(CASE WHEN journal != '' THEN 1 END) as has_journal,
                COUNT(CASE WHEN year IS NOT NULL THEN 1 END) as has_year,
                COUNT(CASE WHEN doi != '' THEN 1 END) as has_doi
            FROM citations
        """)
        quality = cursor.fetchone()
        print(f"\n7. Data Quality Check:")
        print(f"   Total: {quality[0]}, Authors: {quality[1]}, Titles: {quality[2]}")
        print(f"   Journals: {quality[3]}, Years: {quality[4]}, DOIs: {quality[5]}")
        
        conn.close()
        
        print(f"\n=== ALL TESTS COMPLETED SUCCESSFULLY ===")
        print(f"Database file: {db_file} ({db_file.stat().st_size // 1024}KB)")
        
    except Exception as e:
        print(f"Error testing database: {e}")

if __name__ == "__main__":
    test_database()