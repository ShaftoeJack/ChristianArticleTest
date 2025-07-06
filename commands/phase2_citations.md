# Phase 2: Citation Analysis & Background Research

## Command Overview
Extract and categorize all citations, research key background sources, and build contextual understanding of the research field.

## Input Requirements
- **Phase 1 Outputs**: All files from phase1_ingestion/
- **Internet Access**: For citation searching and downloading
- **Working Directory**: `Working_Docs/` structure

## Dependencies
- Phase 1 must be completed successfully
- `article_text.txt` must be available for citation extraction

## Objectives
- Extract and categorize all citations
- Research key background sources
- Build contextual understanding of the research field

## Processing Steps

### 2.1 Citation Extraction and SQLite Database Creation
- **Action**: Extract all citations from References section and create SQLite database for efficient querying
- **Database Creation**: Initialize SQLite database with required schema:
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
      pdf_available BOOLEAN DEFAULT 0,
      txt_available BOOLEAN DEFAULT 0,
      category TEXT,
      file_path TEXT,
      search_attempts TEXT,
      availability_status TEXT DEFAULT 'pending'
  );
  
  -- Create indexes for efficient querying
  CREATE INDEX idx_priority_score ON citations(priority_score DESC);
  CREATE INDEX idx_top15 ON citations(top_15_priority);
  CREATE INDEX idx_year ON citations(year);
  CREATE INDEX idx_category ON citations(category);
  CREATE INDEX idx_pdf_available ON citations(pdf_available);
  CREATE INDEX idx_introduction_mention ON citations(introduction_mention);
  ```

- **Advanced Option**: For comprehensive citation extraction, use Gemini CLI:
  ```bash
  gemini --yolo -p "@Working_Docs/phase1_ingestion/article_text.txt Extract all citations from the References section and format them as structured data with authors, title, journal, year, volume, issue, pages, DOI, and URL where available. Save to Working_Docs/phase2_citations/citations_raw.json for database import"
  ```
- **Alternative**: Direct PDF citation extraction:
  ```bash
  gemini --yolo -p "@document.pdf Extract all citations from the References section and format them as structured data with complete bibliographic information including DOI and PMID where available"
  ```
- **Output**: 
  - `Working_Docs/phase2_citations/citations_database.sqlite` - Main SQLite database
  - `Working_Docs/phase2_citations/citations_raw.json` - Raw extraction data (for backup)
  
- **Database Import Process**:
  1. Extract citations to JSON format
  2. Parse and clean bibliographic data
  3. Insert into SQLite database with proper data types
  4. Initialize all boolean and status fields

### 2.2 Citation Frequency Analysis & Priority Scoring
- **Action**: Analyze citation usage patterns in main article text and update SQLite database
- **Database Update Process**:
  ```sql
  -- Update frequency and priority data
  UPDATE citations SET 
      main_text_frequency = [count],
      introduction_mention = [1 or 0],
      recent_publication = CASE WHEN year >= (2023 - 5) THEN 1 ELSE 0 END,
      doi_available = CASE WHEN doi IS NOT NULL AND doi != '' THEN 1 ELSE 0 END,
      priority_score = (
          CASE WHEN introduction_mention = 1 THEN 3 ELSE 0 END +
          main_text_frequency +
          CASE WHEN recent_publication = 1 THEN 1 ELSE 0 END +
          CASE WHEN doi_available = 1 THEN 1 ELSE 0 END
      )
  WHERE id = [citation_id];
  ```

- **Frequency Counting Process**:
  1. **Count Main Text Citations**: Search article text for each citation reference (e.g., "Smith et al., 2018")
  2. **Identify Introduction Citations**: Note which citations appear in Introduction section
  3. **Update Database**: Use SQL UPDATE statements to populate frequency and boolean fields
  4. **Calculate Priority Score**: Automated calculation using SQL formula above

- **Priority Score Formula**:
  - Introduction citation = +3 points
  - Each additional main text mention = +1 point
  - Recent publication (last 5 years) = +1 point
  - DOI available = +1 point

- **Priority Score Examples**:
  - Citation in Introduction + 4 main text mentions + recent + DOI = 9 points
  - Citation only in Discussion + 1 mention + older + no DOI = 2 points

### 2.3 Citation Categorization
- **Categories** (assign after frequency analysis):
  - **Foundational**: Establishes basic principles or background knowledge
  - **Methodological**: Describes techniques, procedures, or analytical methods
  - **Comparative**: Similar studies, contrasting findings, or related research
  - **Recent Developments**: Current state of field, latest discoveries
  - **Theoretical**: Conceptual frameworks or theoretical models

### 2.4 Strategic Citation Collection - Top 15 Approach

**Collection Strategy** (REVISED for efficiency):
- **Target**: Collect only TOP 15 highest-priority citations
- **Selection Process**:
  1. Rank all citations by priority score (highest first)
  2. Select top 15 citations for active collection
  3. Document remaining citations for potential later acquisition
  4. Focus collection efforts on these 15 most critical sources

**Rationale for Top 15 Limit**:
- Balances thorough analysis with time efficiency
- Captures most frequently-cited and foundational sources
- Reduces collection time from hours to ~30-45 minutes
- Allows just-in-time collection if gaps identified during analysis

**Search Strategy** (in order of priority):
1. **DOI Resolution**: Use DOI to access article directly
2. **PubMed/PMC Search**: Search using PMID or title/authors
3. **Google Scholar**: Broad academic search
4. **Publisher Websites**: Direct journal searches
5. **Preprint Servers**: arXiv, bioRxiv, medRxiv, etc.
6. **Academic Databases**: Semantic Scholar, CORE, etc.

**Download Attempts** (for Top 15 only):
- Try open access versions first
- Check institutional access if available
- Look for author-deposited versions
- Search for preprint versions

**Search Documentation**:
- Record search attempts, sources checked, and outcomes for Top 15 citations
- Note success rate and access patterns
- Identify which citation types are most/least available

### 2.5 Just-in-Time Citation Collection
**Process**: If analysis in Phases 3-5 reveals critical knowledge gaps requiring specific citations:
1. **Gap Identification**: Document specific citation needed and why
2. **Targeted Collection**: Attempt to obtain the specific required citation
3. **Impact Assessment**: Evaluate how missing citation affects analysis quality
4. **Documentation**: Record additional collection attempts and outcomes

**Trigger Conditions for Additional Collection**:
- Phase 3: Key concept requires definition from specific source
- Phase 4: Technical methodology needs clarification from cited method paper
- Phase 5: Significance claims need validation from comparative studies

**Output**: 
- Downloaded articles: `Working_Docs/phase2_citations/downloaded_articles/[citation_id]_[author_year].pdf`
- Search log: `Working_Docs/phase2_citations/search_log.json`

### 2.6 Unavailable Article Reporting
- **Action**: Document articles that could not be obtained
- **Criteria for "Unavailable"**: 
  - No open access version found
  - Behind paywall with no institutional access
  - Not digitally available
  - Broken or invalid DOI/links
  - Article retracted or removed

- **Output**: `Working_Docs/phase2_citations/unavailable_articles_report.md`
- **Enhanced Format** (focused on Top 15):
```markdown
# Unavailable Articles Report - Top 15 Priority Citations

## Summary
- Total citations in paper: [N]
- Top 15 priority citations selected based on frequency and introduction mentions
- Successfully downloaded from Top 15: [N]
- Unavailable from Top 15: [N]
- Success rate for priority citations: [%]

## Priority Citation Status

### Successfully Obtained (Top 15)
1. **Author, Year** - "Title" (Priority Score: X)
   - Status: Downloaded/Available
   - File: `downloaded_articles/citation_01_author_year.pdf`

### Unavailable Priority Citations (Top 15)
1. **Author, Year** - "Title" (Priority Score: X) 
   - Journal: Journal Name
   - DOI: 10.xxxx/xxxx
   - Introduction mention: Yes/No
   - Main text frequency: X mentions
   - Reason unavailable: Behind paywall/Access denied
   - Search attempts: [list sources tried]
   - Suggested filename: citation_02_author_year_keywords.pdf
   - Impact on analysis: High/Medium/Low

## Instructions for User
**Priority Focus**: The Top 15 citations listed above are most critical for analysis.
Please place any manually obtained articles in:
`Working_Docs/user_provided_articles/`

Use the suggested filenames above for consistency.

## Remaining Citations (Not Actively Collected)
- [N] additional citations available for just-in-time collection if needed
- These will be collected only if specific knowledge gaps identified during analysis
- See `citations_index.json` for complete list with priority scores
```

### 2.7 User-Provided Article Integration
- **Action**: Check for and integrate any user-provided articles
- **Process**:
  1. Scan `Working_Docs/user_provided_articles/` directory
  2. Match filenames to unavailable articles list
  3. Update citations_index.json with new file paths
  4. Move integrated articles to appropriate phase2 folders
- **Output**: Updated `citations_index.json` with availability status

### 2.8 Priority Citation Analysis
- **Action**: Select 10-15 most critical citations for deep analysis
- **Priority Criteria**: 
  - Frequently cited in the main article
  - Foundational to the argument
  - Methodologically important
  - Recent and relevant developments
  - Successfully downloaded (prioritize available full texts)

- **Analysis Method**: 
  - Full text analysis for downloaded articles
  - Abstract/summary analysis for unavailable articles
  - Cross-reference with main article claims

- **Output**: `Working_Docs/phase2_citations/citation_summaries.md`

### 2.9 Background Context Development
- **Action**: **ULTRATHINK** - Synthesize citation research into coherent background understanding
- **Advanced Option**: For backup research when citations are unavailable, use Gemini CLI:
  ```bash
  gemini -p "Perform a web search for recent review articles (published since 2020) on [research topic from main article]"
  gemini -p "Search for articles that discuss the [main article title/authors] to see how it was received in the scientific community"
  ```
- **Consider**: Knowledge gaps from unavailable articles and how they might affect understanding
- **Output**: `Working_Docs/phase2_citations/background_context.md`
- **Include**: 
  - Field overview based on available sources
  - Current state of knowledge
  - Key debates and methodological approaches
  - Acknowledgment of knowledge gaps from unavailable sources
- **Documentation**: Record research decisions, source reliability assessments, impact of missing sources

## Quality Assurance Checkpoints
Before proceeding to next phase:
- [ ] All citations extracted and categorized
- [ ] Search strategy executed for priority citations
- [ ] Unavailable articles documented with priority levels
- [ ] Background context developed from available sources
- [ ] Knowledge gaps identified and documented
- [ ] Process thoroughly documented

## Output Files
- `Working_Docs/phase2_citations/citations_index.json` - Complete citation database
- `Working_Docs/phase2_citations/downloaded_articles/` - Successfully obtained articles
- `Working_Docs/phase2_citations/search_log.json` - Search attempt documentation
- `Working_Docs/phase2_citations/unavailable_articles_report.md` - Missing articles report
- `Working_Docs/phase2_citations/citation_summaries.md` - Analysis of priority citations
- `Working_Docs/phase2_citations/background_context.md` - Field context synthesis

## Success Criteria
- Citation extraction >95% complete
- Priority citations identified and analyzed
- Background context developed from available sources
- Knowledge gaps clearly documented
- Search strategy executed systematically
- Quality documentation complete

## Error Handling
- If citation extraction fails, attempt manual parsing
- If searches fail, document and continue with available sources
- If background context is limited, acknowledge gaps explicitly
- Always document limitations and their potential impact

## Next Phase Prerequisites
- Citations extracted and categorized
- Background context established
- Priority citations analyzed
- Knowledge gaps identified
- Quality checkpoints passed