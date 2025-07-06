# Citations Database Documentation

## Overview
The large citations_index.json file (457KB, 578 citations) has been successfully converted to an efficient SQLite database for better context management during analysis phases.

## Database Files
- **citations_database.sqlite** (225KB) - Main SQLite database containing all citations
- **sqlite_query_examples.sql** - Comprehensive collection of useful SQL queries
- **citations_query.py** - Command-line utility for common database operations
- **convert_to_sqlite.py** - Original conversion script (for reference)
- **test_database.py** - Comprehensive database functionality tests
- **verify_conversion.py** - Data integrity verification script

## Database Structure
```sql
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
);
```

## Indexes for Performance
- `idx_priority_score` - Priority score descending
- `idx_top15` - Top 15 priority citations
- `idx_year` - Publication year
- `idx_authors` - Author names
- `idx_doi` - DOI field
- `idx_category` - Citation category

## Quick Usage Examples

### Command Line Tool
```bash
# Show database statistics
python citations_query.py stats

# Get top 10 priority citations
python citations_query.py top --limit 10

# Find citations by author
python citations_query.py author --author "Smith"

# Get recent publications
python citations_query.py recent --start-year 2020 --end-year 2023

# Search by journal
python citations_query.py journal --journal "Nature"
```

### Direct SQLite Queries
```bash
# Basic count
sqlite3 citations_database.sqlite "SELECT COUNT(*) FROM citations;"

# Top priority citations
sqlite3 citations_database.sqlite "SELECT authors, title, priority_score FROM citations WHERE top_15_priority = 1 ORDER BY priority_score DESC;"

# Export to CSV
sqlite3 citations_database.sqlite -csv -header "SELECT * FROM citations WHERE top_15_priority = 1;" > top15_citations.csv
```

## Key Benefits

### Context Efficiency
- **Original JSON**: 457KB, loads entire file into memory
- **SQLite Database**: 225KB, query only needed citations
- **Context Savings**: ~50% reduction in size, unlimited query flexibility

### Performance Improvements
- **Indexed Searches**: Fast lookups by priority, author, year, journal
- **Selective Queries**: Get only relevant citations for specific analysis tasks
- **SQL Flexibility**: Complex queries for advanced analysis

### Analysis Integration
- **Phase 3**: Query citations by research themes or methodologies
- **Phase 4**: Analyze citation patterns, temporal trends, journal distributions
- **Phase 5**: Generate bibliography entries, reference lists, citation networks

## Data Integrity Verification
✅ All 578 citations successfully transferred  
✅ All fields preserved with correct data types  
✅ All boolean flags maintained  
✅ Priority scores and rankings intact  
✅ DOI and URL information preserved  

## Common Query Patterns

### Research Focus Queries
```sql
-- High-priority foundational citations
SELECT * FROM citations WHERE priority_score > 50 ORDER BY priority_score DESC;

-- Recent developments in the field
SELECT * FROM citations WHERE year >= 2018 ORDER BY year DESC;

-- Key introductory references
SELECT * FROM citations WHERE introduction_mention = 1 ORDER BY priority_score DESC;
```

### Publication Analysis
```sql
-- Most productive journals
SELECT journal, COUNT(*) as count FROM citations GROUP BY journal ORDER BY count DESC;

-- Citation timeline
SELECT year, COUNT(*) as count FROM citations GROUP BY year ORDER BY year;

-- Author productivity
SELECT authors, COUNT(*) as count FROM citations GROUP BY authors HAVING count > 1;
```

### Research Accessibility
```sql
-- Available full-text sources
SELECT * FROM citations WHERE doi_available = 1 AND doi != '';

-- URLs for web access
SELECT * FROM citations WHERE url != '' ORDER BY priority_score DESC;
```

## Future Enhancements
- Citation network analysis tables
- Full-text search capabilities
- Automated citation formatting
- Reference management integration
- Research gap identification queries

## Technical Notes
- Database uses UTF-8 encoding for international characters
- Boolean fields stored as INTEGER (0/1)
- All text fields support full Unicode
- Year field stored as INTEGER for efficient range queries
- Priority scores enable weighted analysis

## Usage in Analysis Phases
This database replaces the large JSON file for all future citation lookups, enabling:
- Targeted citation retrieval for specific research questions
- Efficient context window management
- Complex analytical queries
- Fast reference generation
- Systematic literature analysis

The database is ready for integration into Phases 3-5 of the analysis workflow.