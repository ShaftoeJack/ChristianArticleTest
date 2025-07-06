#!/usr/bin/env python3
"""
Command-line utility for querying the citations database
Usage: python citations_query.py [command] [options]
"""

import sqlite3
import argparse
import sys
from pathlib import Path

def connect_database():
    """Connect to the citations database"""
    db_file = Path("citations_database.sqlite")
    if not db_file.exists():
        print(f"Error: Database file not found: {db_file}")
        sys.exit(1)
    return sqlite3.connect(db_file)

def query_top_priority(limit=15):
    """Get top priority citations"""
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, authors, title, journal, year, priority_score, doi
        FROM citations 
        WHERE top_15_priority = 1 
        ORDER BY priority_score DESC 
        LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    print(f"Top {limit} Priority Citations:")
    print("-" * 80)
    for i, (id, authors, title, journal, year, score, doi) in enumerate(results, 1):
        print(f"{i:2d}. {authors} ({year}) - Priority: {score}")
        print(f"    Title: {title}")
        print(f"    Journal: {journal}")
        if doi:
            print(f"    DOI: {doi}")
        print()

def query_by_author(author_name):
    """Find citations by author name"""
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, authors, title, journal, year, priority_score
        FROM citations 
        WHERE authors LIKE ? 
        ORDER BY priority_score DESC
    """, (f"%{author_name}%",))
    
    results = cursor.fetchall()
    conn.close()
    
    print(f"Citations by '{author_name}':")
    print("-" * 80)
    for i, (id, authors, title, journal, year, score) in enumerate(results, 1):
        print(f"{i:2d}. {authors} ({year}) - Priority: {score}")
        print(f"    Title: {title}")
        print(f"    Journal: {journal}")
        print()

def query_recent(start_year=2018, end_year=2023):
    """Get recent publications"""
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, authors, title, journal, year, priority_score, doi
        FROM citations 
        WHERE year >= ? AND year <= ?
        ORDER BY year DESC, priority_score DESC
    """, (start_year, end_year))
    
    results = cursor.fetchall()
    conn.close()
    
    print(f"Recent Publications ({start_year}-{end_year}):")
    print("-" * 80)
    for i, (id, authors, title, journal, year, score, doi) in enumerate(results, 1):
        print(f"{i:2d}. {authors} ({year}) - Priority: {score}")
        print(f"    Title: {title}")
        print(f"    Journal: {journal}")
        if doi:
            print(f"    DOI: {doi}")
        print()

def query_by_journal(journal_name):
    """Find citations by journal name"""
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, authors, title, journal, year, priority_score
        FROM citations 
        WHERE journal LIKE ? 
        ORDER BY year DESC, priority_score DESC
    """, (f"%{journal_name}%",))
    
    results = cursor.fetchall()
    conn.close()
    
    print(f"Citations from '{journal_name}':")
    print("-" * 80)
    for i, (id, authors, title, journal, year, score) in enumerate(results, 1):
        print(f"{i:2d}. {authors} ({year}) - Priority: {score}")
        print(f"    Title: {title}")
        print(f"    Journal: {journal}")
        print()

def query_statistics():
    """Show database statistics"""
    conn = connect_database()
    cursor = conn.cursor()
    
    # Basic stats
    cursor.execute("SELECT COUNT(*) FROM citations")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM citations WHERE top_15_priority = 1")
    top15 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM citations WHERE doi_available = 1")
    with_doi = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM citations WHERE year >= 2018")
    recent = cursor.fetchone()[0]
    
    # Priority stats
    cursor.execute("""
        SELECT MIN(priority_score), MAX(priority_score), AVG(priority_score)
        FROM citations
    """)
    min_p, max_p, avg_p = cursor.fetchone()
    
    # Year stats
    cursor.execute("""
        SELECT MIN(year), MAX(year), AVG(year)
        FROM citations WHERE year IS NOT NULL
    """)
    min_y, max_y, avg_y = cursor.fetchone()
    
    # Top journals
    cursor.execute("""
        SELECT journal, COUNT(*) as count
        FROM citations 
        WHERE journal != ''
        GROUP BY journal 
        ORDER BY count DESC 
        LIMIT 5
    """)
    top_journals = cursor.fetchall()
    
    conn.close()
    
    print("Database Statistics:")
    print("=" * 50)
    print(f"Total citations: {total}")
    print(f"Top 15 priority: {top15}")
    print(f"With DOI: {with_doi}")
    print(f"Recent (2018+): {recent}")
    print()
    print(f"Priority scores: {min_p} - {max_p} (avg: {avg_p:.1f})")
    print(f"Publication years: {min_y} - {max_y} (avg: {avg_y:.1f})")
    print()
    print("Top 5 Journals:")
    for journal, count in top_journals:
        print(f"  {journal}: {count} citations")

def main():
    parser = argparse.ArgumentParser(description='Query the citations database')
    parser.add_argument('command', choices=['top', 'author', 'recent', 'journal', 'stats'], 
                       help='Query command to execute')
    parser.add_argument('--limit', type=int, default=15, 
                       help='Limit number of results (default: 15)')
    parser.add_argument('--author', type=str, 
                       help='Author name to search for')
    parser.add_argument('--journal', type=str, 
                       help='Journal name to search for')
    parser.add_argument('--start-year', type=int, default=2018,
                       help='Start year for recent publications (default: 2018)')
    parser.add_argument('--end-year', type=int, default=2023,
                       help='End year for recent publications (default: 2023)')
    
    args = parser.parse_args()
    
    if args.command == 'top':
        query_top_priority(args.limit)
    elif args.command == 'author':
        if not args.author:
            print("Error: --author required for author search")
            sys.exit(1)
        query_by_author(args.author)
    elif args.command == 'recent':
        query_recent(args.start_year, args.end_year)
    elif args.command == 'journal':
        if not args.journal:
            print("Error: --journal required for journal search")
            sys.exit(1)
        query_by_journal(args.journal)
    elif args.command == 'stats':
        query_statistics()

if __name__ == "__main__":
    main()