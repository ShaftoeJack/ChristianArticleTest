-- SQLite Query Examples for Citations Database
-- Database: citations_database.sqlite
-- Table: citations

-- ===========================================
-- BASIC QUERIES
-- ===========================================

-- Get all citations count
SELECT COUNT(*) AS total_citations FROM citations;

-- Get database schema
.schema citations

-- Show table info
.tables

-- ===========================================
-- PRIORITY-BASED QUERIES
-- ===========================================

-- Top 15 priority citations (highest priority first)
SELECT id, authors, title, journal, year, priority_score
FROM citations 
WHERE top_15_priority = 1
ORDER BY priority_score DESC;

-- All citations by priority score (descending)
SELECT id, authors, title, journal, year, priority_score
FROM citations 
ORDER BY priority_score DESC
LIMIT 50;

-- Citations with high main text frequency (>= 5 mentions)
SELECT id, authors, title, journal, year, main_text_frequency
FROM citations 
WHERE main_text_frequency >= 5
ORDER BY main_text_frequency DESC;

-- ===========================================
-- AUTHOR-BASED QUERIES
-- ===========================================

-- Find citations by specific author (case-insensitive)
SELECT id, authors, title, journal, year
FROM citations 
WHERE authors LIKE '%Smith%'
ORDER BY year DESC;

-- Find citations by multiple authors
SELECT id, authors, title, journal, year
FROM citations 
WHERE authors LIKE '%Johnson%' OR authors LIKE '%Brown%'
ORDER BY year DESC;

-- Get unique author list (first author only)
SELECT DISTINCT SUBSTR(authors, 1, INSTR(authors || ',', ',') - 1) AS first_author
FROM citations
WHERE authors != ''
ORDER BY first_author;

-- ===========================================
-- TEMPORAL QUERIES
-- ===========================================

-- Recent publications (2018-2023)
SELECT id, authors, title, journal, year
FROM citations 
WHERE year >= 2018 AND year <= 2023
ORDER BY year DESC;

-- Publications by decade
SELECT 
    CASE 
        WHEN year >= 2020 THEN '2020s'
        WHEN year >= 2010 THEN '2010s'
        WHEN year >= 2000 THEN '2000s'
        WHEN year >= 1990 THEN '1990s'
        ELSE 'Earlier'
    END AS decade,
    COUNT(*) AS citation_count
FROM citations 
WHERE year IS NOT NULL
GROUP BY decade
ORDER BY decade DESC;

-- Publications by year (recent years only)
SELECT year, COUNT(*) AS citation_count
FROM citations 
WHERE year >= 2010
GROUP BY year
ORDER BY year DESC;

-- ===========================================
-- JOURNAL-BASED QUERIES
-- ===========================================

-- Most cited journals
SELECT journal, COUNT(*) AS citation_count
FROM citations 
WHERE journal != ''
GROUP BY journal
ORDER BY citation_count DESC
LIMIT 20;

-- Find citations from specific journal
SELECT id, authors, title, year, volume, issue, pages
FROM citations 
WHERE journal LIKE '%Nature%'
ORDER BY year DESC;

-- ===========================================
-- DOI AND URL QUERIES
-- ===========================================

-- Citations with DOIs available
SELECT id, authors, title, journal, year, doi
FROM citations 
WHERE doi_available = 1 AND doi != ''
ORDER BY year DESC;

-- Citations without DOIs
SELECT id, authors, title, journal, year
FROM citations 
WHERE doi_available = 0 OR doi = ''
ORDER BY priority_score DESC;

-- Citations with URLs but no DOIs
SELECT id, authors, title, journal, year, url
FROM citations 
WHERE url != '' AND (doi = '' OR doi IS NULL)
ORDER BY year DESC;

-- ===========================================
-- RESEARCH FOCUS QUERIES
-- ===========================================

-- Citations mentioned in introduction
SELECT id, authors, title, journal, year, priority_score
FROM citations 
WHERE introduction_mention = 1
ORDER BY priority_score DESC;

-- High-priority recent publications with DOIs
SELECT id, authors, title, journal, year, doi, priority_score
FROM citations 
WHERE recent_publication = 1 
    AND doi_available = 1 
    AND priority_score >= 50
ORDER BY priority_score DESC;

-- ===========================================
-- TEXT SEARCH QUERIES
-- ===========================================

-- Search titles for specific terms
SELECT id, authors, title, journal, year
FROM citations 
WHERE title LIKE '%machine learning%' OR title LIKE '%artificial intelligence%'
ORDER BY year DESC;

-- Search titles and authors for keywords
SELECT id, authors, title, journal, year
FROM citations 
WHERE title LIKE '%neural%' OR authors LIKE '%Neural%'
ORDER BY priority_score DESC;

-- ===========================================
-- STATISTICAL QUERIES
-- ===========================================

-- Priority score statistics
SELECT 
    MIN(priority_score) AS min_priority,
    MAX(priority_score) AS max_priority,
    AVG(priority_score) AS avg_priority,
    COUNT(*) AS total_citations
FROM citations;

-- Publication year statistics
SELECT 
    MIN(year) AS earliest_year,
    MAX(year) AS latest_year,
    AVG(year) AS avg_year,
    COUNT(*) AS total_with_year
FROM citations 
WHERE year IS NOT NULL;

-- Main text frequency statistics
SELECT 
    MIN(main_text_frequency) AS min_frequency,
    MAX(main_text_frequency) AS max_frequency,
    AVG(main_text_frequency) AS avg_frequency,
    COUNT(*) AS total_citations
FROM citations;

-- ===========================================
-- COMPLEX ANALYTICAL QUERIES
-- ===========================================

-- Top authors by citation count
SELECT 
    SUBSTR(authors, 1, INSTR(authors || ',', ',') - 1) AS first_author,
    COUNT(*) AS citation_count,
    AVG(priority_score) AS avg_priority
FROM citations
WHERE authors != ''
GROUP BY first_author
HAVING citation_count > 1
ORDER BY citation_count DESC, avg_priority DESC;

-- Research timeline: citations by 5-year periods
SELECT 
    CASE 
        WHEN year >= 2020 THEN '2020-2024'
        WHEN year >= 2015 THEN '2015-2019'
        WHEN year >= 2010 THEN '2010-2014'
        WHEN year >= 2005 THEN '2005-2009'
        WHEN year >= 2000 THEN '2000-2004'
        ELSE 'Pre-2000'
    END AS period,
    COUNT(*) AS citation_count,
    AVG(priority_score) AS avg_priority
FROM citations 
WHERE year IS NOT NULL
GROUP BY period
ORDER BY period DESC;

-- High-impact recent research (recent + high priority + DOI)
SELECT id, authors, title, journal, year, doi, priority_score
FROM citations 
WHERE year >= 2015 
    AND priority_score >= 30 
    AND doi_available = 1
ORDER BY priority_score DESC, year DESC;

-- ===========================================
-- UTILITY QUERIES
-- ===========================================

-- Export top 15 citations for reference
SELECT 
    authors,
    title,
    journal,
    year,
    volume,
    issue,
    pages,
    doi,
    priority_score
FROM citations 
WHERE top_15_priority = 1
ORDER BY priority_score DESC;

-- Quick citation format for bibliography
SELECT 
    authors || ' (' || year || '). ' || title || '. ' || journal || 
    CASE 
        WHEN volume != '' THEN ', ' || volume
        ELSE ''
    END ||
    CASE 
        WHEN issue != '' THEN '(' || issue || ')'
        ELSE ''
    END ||
    CASE 
        WHEN pages != '' THEN ', ' || pages
        ELSE ''
    END ||
    CASE 
        WHEN doi != '' THEN '. DOI: ' || doi
        ELSE ''
    END AS formatted_citation
FROM citations 
WHERE top_15_priority = 1
ORDER BY priority_score DESC;

-- ===========================================
-- MAINTENANCE QUERIES
-- ===========================================

-- Check for duplicate titles
SELECT title, COUNT(*) as count
FROM citations 
WHERE title != ''
GROUP BY title 
HAVING count > 1;

-- Check data quality
SELECT 
    COUNT(*) as total_citations,
    COUNT(CASE WHEN authors != '' THEN 1 END) as has_authors,
    COUNT(CASE WHEN title != '' THEN 1 END) as has_title,
    COUNT(CASE WHEN journal != '' THEN 1 END) as has_journal,
    COUNT(CASE WHEN year IS NOT NULL THEN 1 END) as has_year,
    COUNT(CASE WHEN doi != '' THEN 1 END) as has_doi
FROM citations;

-- Find incomplete records
SELECT id, authors, title, journal, year, doi
FROM citations 
WHERE authors = '' OR title = '' OR journal = '' OR year IS NULL
ORDER BY priority_score DESC;

-- ===========================================
-- COMMAND LINE USAGE EXAMPLES
-- ===========================================

-- To run these queries from command line:
-- sqlite3 citations_database.sqlite "SELECT COUNT(*) FROM citations;"
-- sqlite3 citations_database.sqlite ".read sqlite_query_examples.sql"
-- sqlite3 citations_database.sqlite -header -column "SELECT * FROM citations WHERE top_15_priority = 1;"

-- To export results to CSV:
-- sqlite3 citations_database.sqlite -csv -header "SELECT * FROM citations WHERE top_15_priority = 1;" > top15_citations.csv

-- To get formatted output:
-- sqlite3 citations_database.sqlite -header -column "SELECT authors, title, year FROM citations WHERE top_15_priority = 1;"