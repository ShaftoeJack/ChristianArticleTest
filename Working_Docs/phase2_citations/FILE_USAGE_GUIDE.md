# File Usage Guide for Analysis Phases (3-5)

## 🚨 **CRITICAL CONTEXT EFFICIENCY GUIDELINES** 🚨

### **File Processing Priority Rules**

#### **✅ USE THESE FILES (Context Efficient)**
```
Working_Docs/phase2_citations/downloaded_articles/
├── citation_XXX_Author_Year.txt  ← **USE THESE FOR ALL ANALYSIS**
└── citations_database.sqlite      ← **QUERY THIS FOR CITATIONS**
```

#### **❌ AVOID THESE FILES (Context Wasteful)**
```
Working_Docs/phase2_citations/downloaded_articles/
├── citation_XXX_Author_Year.pdf  ← **NEVER USE - WASTE OF CONTEXT**
└── citations_index.json          ← **LEGACY FILE - TOO LARGE**
```

---

## **Detailed File Usage Instructions**

### **📄 Text Files (.txt) - PRIMARY SOURCES**
**Location**: `Working_Docs/phase2_citations/downloaded_articles/*.txt`
**Count**: 17 processed articles
**Usage**: Direct content analysis for all phases

**Why Use TXT Files**:
- ✅ **Pre-processed**: Clean text extraction already completed
- ✅ **Context optimized**: Smaller file sizes, faster loading
- ✅ **Analysis ready**: Formatted for computational processing
- ✅ **Quality verified**: All extractions rated "Excellent"

**File Naming Convention**:
```
citation_003_A_2020.txt          ← Allen et al. 2020
citation_010_Angielczyk_2017.txt ← Angielczyk & Kammerer 2017
citation_012_Angielczyk_2017.txt ← Angielczyk et al. 2017 (Sangusaurus)
citation_013_Angielczyk_2021.txt ← Angielczyk et al. 2021 (Kunpania)
... (all 17 files follow this pattern)
```

### **🗄️ SQLite Database - CITATION QUERIES**
**Location**: `Working_Docs/phase2_citations/citations_database.sqlite`
**Records**: 578 citations with complete metadata
**Usage**: Efficient citation lookups without loading massive JSON

**Key Benefits**:
- ✅ **Context efficient**: Query specific citations only
- ✅ **Fast searches**: Indexed database vs. linear JSON parsing
- ✅ **Flexible queries**: SQL for complex analysis needs
- ✅ **Selective loading**: Get only what you need when you need it

**Common Query Examples**:
```sql
-- Get top 15 priority citations
SELECT * FROM citations WHERE top_15_priority = 1 ORDER BY priority_score DESC;

-- Find citations by specific author
SELECT * FROM citations WHERE authors LIKE '%Angielczyk%';

-- Get recent publications
SELECT * FROM citations WHERE year >= 2018 ORDER BY year DESC;

-- Find citations with DOIs
SELECT * FROM citations WHERE doi_available = 1;
```

### **📁 PDF Files - AVOID IN ANALYSIS PHASES**
**Location**: `Working_Docs/phase2_citations/downloaded_articles/*.pdf`
**Status**: Archive only - do not process
**Reason**: Context inefficient when TXT alternatives exist

**Why Avoid PDFs**:
- ❌ **Context waste**: Large file sizes consume unnecessary space
- ❌ **Processing overhead**: Require additional extraction steps
- ❌ **Redundant**: TXT files already contain the same content
- ❌ **Analysis inefficient**: Not optimized for computational processing

---

## **Phase-Specific Usage Guidelines**

### **Phase 3: Preliminary Analysis**
**Primary Sources**:
- `Working_Docs/phase1_ingestion/article_text.txt` (main article)
- `Working_Docs/phase2_citations/downloaded_articles/*.txt` (background literature)
- SQLite queries for citation context

**Workflow**:
1. Read main article for comprehensive understanding
2. Query database for priority citations: `SELECT * FROM citations WHERE top_15_priority = 1`
3. Read relevant TXT files for background context
4. Cross-reference using citation IDs for systematic analysis

### **Phase 4: Deep Sectional Analysis**
**Primary Sources**:
- `Working_Docs/phase1_ingestion/article_text.txt` (section-by-section analysis)
- Selected TXT files based on section relevance
- SQLite queries for methodology and comparative studies

**Workflow**:
1. Analyze main article sections systematically
2. Query for relevant citations: `SELECT * FROM citations WHERE category = 'methodological'`
3. Read corresponding TXT files for technical context
4. Cross-reference findings with comparative studies

### **Phase 5: Synthesis & General Audience Translation**
**Primary Sources**:
- All previous phase outputs
- Selected TXT files for significance validation
- SQLite queries for foundational and recent developments

**Workflow**:
1. Synthesize findings from all previous phases
2. Query for foundational work: `SELECT * FROM citations WHERE introduction_mention = 1`
3. Validate significance claims against literature
4. Create accessible explanations using background context

---

## **Quick Reference Commands**

### **SQLite Database Queries**
```bash
# Command line access
sqlite3 Working_Docs/phase2_citations/citations_database.sqlite

# Python utility (if available)
python Working_Docs/phase2_citations/citations_query.py stats
python Working_Docs/phase2_citations/citations_query.py top --limit 15
```

### **File Counting**
```bash
# Count available TXT files
ls Working_Docs/phase2_citations/downloaded_articles/*.txt | wc -l

# Check specific citation file
ls Working_Docs/phase2_citations/downloaded_articles/citation_289_*
```

### **Cross-Reference Lookup**
```sql
-- Find file for specific citation ID
SELECT id, authors, year, title FROM citations WHERE id = 289;

-- Result tells you to look for: citation_289_King_1988.txt
```

---

## **Context Window Management**

### **Best Practices**
1. **Query first**: Use SQLite to identify relevant citations before reading files
2. **Read selectively**: Only load TXT files needed for current analysis step
3. **Batch efficiently**: Group related citations for single reading session
4. **Cross-reference systematically**: Use citation IDs to maintain organization

### **Efficiency Gains**
- **50% size reduction**: SQLite vs. JSON for citation data
- **Targeted loading**: Read 1-3 TXT files vs. entire literature collection
- **Query precision**: Get exactly the citations needed for current analysis
- **Context preservation**: More space for actual analysis vs. data loading

---

## **Error Prevention**

### **Common Mistakes to Avoid**
❌ Loading PDF files when TXT alternatives exist
❌ Loading entire citations_index.json file
❌ Reading all 17 TXT files simultaneously
❌ Ignoring the SQLite database for citation lookups

### **Recommended Approach**
✅ Start with SQLite query to identify relevant citations
✅ Read specific TXT files based on analysis needs
✅ Use citation IDs for systematic cross-referencing
✅ Maintain efficient context window usage throughout

---

## **File Inventory Summary**

### **Available for Analysis (Context Efficient)**
- **Main Article**: `article_text.txt` (100,494 words)
- **Literature**: 17 TXT files (processed background sources)
- **Citation Database**: SQLite with 578 records
- **Cross-Reference**: File mapping and documentation

### **Archive Only (Context Inefficient)**
- **PDF Files**: 17 PDF files (keep for reference, don't analyze)
- **Legacy JSON**: `citations_index.json` (superseded by SQLite)

### **Total Analysis Capacity**
With efficient file usage, you have comprehensive coverage of:
- **Primary research**: Complete dicynodont fossil study
- **Literature foundation**: 17 key research papers
- **Citation context**: 578 background references
- **Systematic organization**: All cross-referenced and queryable

**Ready for efficient, comprehensive analysis across Phases 3-5!**