# Scientific Article Analysis Orchestrator

## Overview
This orchestrator provides an interactive framework for Claude Code to execute a systematic 5-phase process for analyzing scientific articles and creating accessible general audience explanations. It preserves the core principles and framework while guiding collaborative execution of modular phase commands.

## Interactive Execution Model
Claude Code will execute this orchestrator by:
1. **Reading this orchestrator document** to understand the framework and principles
2. **Reading FILE_USAGE_GUIDE.md** for context efficiency guidelines
3. **Walking through each phase interactively** with the user
4. **Applying quality checkpoints** before proceeding to next phases
5. **Maintaining systematic documentation** throughout the process
6. **Adapting execution** based on article complexity and user preferences

## Core Principles
- **Systematic Approach**: Each phase builds upon the previous one
- **Deep Analysis**: Use "ultrathink" reasoning for all summarization tasks
- **Documentation**: Create detailed records of all steps and decisions
- **Accessibility**: Transform complex scientific concepts into general audience language
- **Quality Assurance**: Built-in checkpoints and validation steps

## Orchestrator Architecture

### Interactive Phase Execution Pattern
```
User: "Please execute the orchestrator for [article.pdf]"

Claude Code:
1. Reads orchestrator.md (this document) for framework
2. Assesses article and determines processing strategy
3. Executes Phase 1 by reading phase1_ingestion.md
4. Shows user results and asks for validation
5. Proceeds to Phase 2 after user approval
6. Continues through all phases with user collaboration
7. Generates final deliverables with user preferences
```

### Interactive Command Structure
```
commands/
├── orchestrator.md          # This framework document for Claude Code
├── phase1_ingestion.md      # Phase 1 command specification
├── phase2_citations.md      # Phase 2 command specification
├── phase3_preliminary.md    # Phase 3 command specification
├── phase4_analysis.md       # Phase 4 command specification
└── phase5_synthesis.md      # Phase 5 command specification
```

### How Claude Code Uses This Structure
1. **Start**: User asks Claude Code to execute the orchestrator
2. **Framework Loading**: Claude reads this orchestrator.md for principles and guidelines
3. **Phase Execution**: Claude reads and executes each phase*.md command interactively
4. **User Collaboration**: Claude asks for user input, approval, and guidance at key points
5. **Quality Validation**: Claude checks phase completion before proceeding

## Article Length Assessment and Strategy

### Length Evaluation Criteria
- **Small** (<8,000 words): Standard processing, read full sections directly
- **Medium** (8,000-20,000 words): Strategic processing, use Task agents for large sections
- **Large** (>20,000 words): Focused processing, sample key sections, extensive use of Task agents

### Processing Strategy Selection
The orchestrator automatically:
1. **Counts words/lines** in extracted text after Phase 1
2. **Identifies longest sections** (especially Results/Methods)
3. **Selects appropriate strategy**:
   - **Full Processing**: Complete analysis of all sections (recommended for <15,000 words)
   - **Strategic Processing**: Full analysis of key sections, sampling of detailed sections
   - **Focused Processing**: Prioritize Abstract, Introduction, Discussion, Conclusions

### Implementation Guidelines
- **Use Task agents** for sections >200 lines
- **Break large Results sections** into logical subsections
- **Maintain systematic approach** regardless of strategy chosen

### Efficiency Improvements
- **PDF Quality Validation**: Automatic quality checks with OCR fallback for non-text PDFs
- **Strategic Citation Collection**: Focus on Top 15 highest-priority citations based on frequency analysis
- **Just-in-Time Collection**: Additional citation gathering only when specific gaps identified
- **Speed Optimization**: pdftotext primary method reduces extraction time from minutes to seconds
- **Context Window Management**: SQLite database and TXT files for efficient access patterns
- **File Usage Guidelines**: Prioritize TXT files over PDFs, avoid large JSON files

### File Processing Priority (CRITICAL)
✅ **USE**: downloaded_articles/*.txt files for literature analysis
✅ **USE**: citations_database.sqlite for citation queries  
❌ **AVOID**: PDF files when TXT alternatives exist
❌ **AVOID**: citations_index.json (too large for context)

**Context Window Management**:
- SQLite queries for targeted citation retrieval
- TXT files for efficient literature analysis
- Batch processing for related citations
- Cross-reference using citation IDs

## Task Agent Usage Guidelines

### When to Use Task Agents
- **Always for Phase 3 and 4**: Complex analysis requiring deep reasoning
- **For large sections** (>200 lines of text)
- **For specialized analysis**: Citation extraction, figure analysis, technical explanations
- **For synthesis tasks**: Integration across multiple documents/phases

### Task Agent Best Practices
1. **Detailed Prompts**: Provide specific instructions including:
   - Exact file paths and line numbers
   - Expected output format and structure
   - Analysis focus areas and methodology
   - Integration requirements with previous phases

2. **ULTRATHINK Requests**: Always explicitly request **ULTRATHINK** methodology for:
   - Phase 3 preliminary analysis
   - Phase 4 sectional analysis
   - Phase 5 synthesis tasks
   - Significance assessments

3. **Parallel Processing**: Use multiple concurrent task agents when possible:
   - Phase 2: Citation extraction + availability search + background analysis
   - Phase 4: Multiple section analyses simultaneously
   - Phase 5: Synthesis + article creation + process documentation

4. **Context Provision**: Always provide task agents with:
   - Background from previous phases
   - Key concepts and definitions established
   - Knowledge gaps identified
   - Overall research significance framework

## File Structure & Temporary File Management

### Working Directory Structure
```
Working_Docs/
├── phase1_ingestion/
│   ├── figures_extracted/        # Extracted images
│   ├── article_text.txt
│   ├── article_structure.json
│   ├── metadata.json
│   └── figures_inventory.json
├── phase2_citations/
│   ├── downloaded_articles/
│   ├── unavailable_articles/
│   ├── citations_index.json
│   ├── search_log.json
│   └── unavailable_articles_report.md
├── phase3_preliminary/
│   ├── initial_summary.md
│   ├── key_concepts.json
│   ├── knowledge_gaps.md
│   └── preliminary_significance.md
├── phase4_analysis/
│   ├── section_analysis_*.md
│   ├── technical_explanations.md
│   └── significance_assessment.md
├── phase5_synthesis/
│   ├── comprehensive_understanding.md
│   ├── general_audience_article.md
│   ├── general_audience_article_revised.md
│   ├── general_audience_article_final.md
│   ├── general_audience_article_final.pdf
│   └── general_audience_article_final.docx
├── process_logs/
│   ├── orchestrator_log.md
│   ├── phase*_log.md
│   └── quality_checkpoints.md
└── user_provided_articles/  # For manually collected citations
```

### Temporary File Types
- **.txt files**: Raw text extraction, notes, lists
- **.md files**: Formatted summaries, analysis, documentation
- **.json files**: Structured data, metadata, indices
- **.ppm/.jpg/.png files**: Extracted figures and images
- **Process logs**: Step-by-step documentation of actions taken

## Interactive Orchestrator Execution Flow

### Phase 1: Article Ingestion & Initial Processing
**Claude Code Actions:**
1. **Read** `commands/phase1_ingestion.md` for detailed instructions
2. **Execute** PDF processing using pdftotext (primary) with quality validation
3. **Quality Check** extracted text for completeness and readability
4. **Fallback to Gemini CLI** if PDF requires OCR processing
5. **Create** all required output files (text, structure, metadata, figures)
6. **Assess** article length and complexity for strategy determination
7. **Present** results to user with quality summary

**User Collaboration Points:**
- Review extracted text quality and completeness (after automatic extraction and validation)
- Confirm article structure identification accuracy
- Validate metadata extraction results
- Approve processing strategy (Full/Strategic/Focused)
- Decide on proceeding to Phase 2

*Note: PDF tools and quality checks happen automatically - user validates results, not tool usage*

### Phase 2: Citation Analysis & Background Research
**Claude Code Actions:**
1. **Read** `commands/phase2_citations.md` for detailed instructions
2. **Execute** citation extraction and frequency analysis
3. **Calculate** priority scores and select Top 15 citations
4. **Perform** strategic citation collection for priority sources
5. **Create** SQLite database and TXT files for efficient access
6. **Document** unavailable Top 15 articles for user collection
7. **Present** citation analysis and research gaps to user

**User Collaboration Points:**
- Review citation extraction and priority scoring accuracy
- Provide any manually collected priority articles (Top 15 focus)
- Confirm background research adequacy based on available sources
- Approve strategic collection approach and knowledge gap assessment
- Validate efficient file structure created (SQLite database, TXT files)
- Decide on proceeding to Phase 3

### Phase 3: Preliminary Analysis
**Claude Code Actions:**
1. **Read** `commands/phase3_preliminary.md` for detailed instructions
2. **Apply** FILE_USAGE_GUIDE.md efficiency guidelines
3. **Execute** ULTRATHINK complete read-through using TXT files
4. **Query** SQLite database for relevant citation context
5. **Identify** key concepts and create accessible definitions
6. **Map** knowledge gaps requiring deeper investigation
7. **Present** preliminary analysis and significance assessment

**User Collaboration Points:**
- Review initial understanding and summary
- Validate key concept identifications
- Confirm knowledge gap priorities
- Approve preliminary significance assessment
- Validate efficient file usage patterns
- Decide on proceeding to Phase 4

### Phase 4: Deep Sectional Analysis
**Claude Code Actions:**
1. **Read** `commands/phase4_analysis.md` for detailed instructions
2. **Apply** FILE_USAGE_GUIDE.md efficiency guidelines
3. **Execute** ULTRATHINK section-by-section analysis using TXT files
4. **Query** SQLite database for methodological and comparative context
5. **Develop** technical concept explanations
6. **Integrate** figure analysis and visual evidence
7. **Cross-reference** systematically using citation IDs
8. **Present** comprehensive significance assessment

**User Collaboration Points:**
- Review sectional analysis depth and accuracy
- Validate technical explanations clarity
- Confirm cross-reference consistency
- Approve comprehensive significance evaluation
- Validate systematic cross-referencing with citation IDs
- Decide on proceeding to Phase 5

### Phase 5: Synthesis & General Audience Translation
**Claude Code Actions:**
1. **Read** `commands/phase5_synthesis.md` for detailed instructions
2. **Apply** FILE_USAGE_GUIDE.md efficiency guidelines
3. **Execute** ULTRATHINK comprehensive synthesis using efficient file access
4. **Validate** significance claims using SQLite database and TXT files
5. **Create** general audience article with validation cycles
6. **Generate** professional documents using MDConverter with updated file paths
7. **Present** final deliverables with quality verification

**User Collaboration Points:**
- Review synthesis completeness and coherence
- Validate general audience article accessibility
- Choose document formatting presets (academic-serif, modern-sans, business-report, etc.)
- Confirm quote integrity and significance calibration
- Validate context-efficient synthesis approach
- Approve final deliverables (after automatic MDConverter execution)

*Note: MDConverter tool executions happen automatically based on chosen presets - user validates outputs*

## Quality Assurance Framework

### Global Quality Standards
- **Accuracy**: All information verified against source material
- **Completeness**: All required outputs generated
- **Consistency**: Alignment across all phases and outputs
- **Accessibility**: General audience comprehension maintained
- **Documentation**: Complete process trail maintained

### Phase Validation Checkpoints
Each phase must pass validation before proceeding:
1. **Output Completeness**: All required files created
2. **Quality Standards**: Content meets phase-specific criteria
3. **Dependency Satisfaction**: Next phase prerequisites met
4. **Documentation**: Process thoroughly recorded

### Error Handling Strategy
- **Phase Failure**: Retry with alternative tools or manual intervention
- **Quality Issues**: Return to previous phase for correction
- **Missing Dependencies**: Install required tools or use alternatives
- **Context Overflow**: Switch to Task agents or Gemini CLI
- **Documentation**: Always record issues and resolutions

## Interactive Orchestrator Commands for Claude Code

### Starting the Interactive Process
**User Request Examples:**
```
"Please execute the orchestrator for article.pdf"
"Start the scientific article analysis protocol for [PDF file]"
"Begin the 5-phase analysis using the orchestrator"
```

**Claude Code Response Pattern:**
1. **Acknowledge** the request and mention reading the orchestrator framework
2. **Ask for** the PDF file location and any initial preferences
3. **Explain** the 5-phase process briefly
4. **Begin** Phase 1 execution after user confirmation

### Phase-by-Phase Execution
**User Control Options:**
```
"Proceed to next phase" - Continue with standard workflow
"Skip to Phase X" - Jump to specific phase (if prerequisites met)
"Pause for review" - Stop for detailed validation
"Restart current phase" - Re-execute current phase with different approach
"Generate interim report" - Create status summary at any point
```

### Collaboration and Validation
**At Each Phase, Claude Code Will:**
- **Show** what was accomplished
- **Highlight** any issues or limitations found
- **Ask** for user validation and approval
- **Wait** for user decision before proceeding
- **Document** all decisions and modifications

## Integration with External Tools

### Primary Tools (Recommended)
- **pdftotext**: Fast, reliable PDF text extraction with quality validation
- **pdfimages**: Figure extraction from PDFs
- **MDConverter**: Professional document generation with presets
- **Claude Code**: Task agents, multi-tool coordination, file analysis

### Secondary Tools
- **Gemini CLI**: OCR processing for non-text PDFs, large document analysis, backup research
- **Basic pandoc**: Document conversion fallback
- **Standard utilities**: grep, jq, find, tar

### Tool Selection Logic
1. **Start with pdftotext** for PDF text extraction with quality checks
2. **Fall back to Gemini CLI** for OCR if quality validation fails
3. **Use SQLite database** for efficient citation queries
4. **Use TXT files** for literature analysis (prioritize over PDFs)
5. **Use MDConverter** for professional document generation
6. **Document tool choices** and success rates
7. **Adapt strategy** based on available tools and PDF characteristics
8. **Apply context window management** best practices throughout

## Success Metrics

The orchestrator succeeds when it produces:
- **Accurate Understanding**: Correct interpretation of scientific content
- **Comprehensive Analysis**: Thorough coverage of all important aspects
- **Accessible Communication**: General audience can understand the significance
- **Complete Documentation**: Full record of process and decisions
- **Quality Output**: Professional-grade deliverables in multiple formats

## Adaptability and Extensions

### Protocol Adaptations
- **Different article types**: Adjust section analysis based on structure
- **Various scientific fields**: Modify citation research and concept explanation
- **Different complexity levels**: Scale background research and analysis depth
- **Multiple audiences**: Generate different format versions

### Extension Points
- **Additional output formats**: Integrate new conversion tools
- **Enhanced analysis**: Add specialized analysis modules
- **Workflow customization**: Allow phase skipping or reordering
- **Quality metrics**: Add quantitative assessment tools

## Getting Started: Instructions for Claude Code

### Initial Orchestrator Execution
When a user asks Claude Code to execute the orchestrator, follow this pattern:

1. **Read and Internalize Framework**
   ```
   "I'll execute the scientific article analysis orchestrator. Let me first read the framework and phase commands to understand the complete protocol."
   ```
   - Read this orchestrator.md file completely
   - Understand the core principles and guidelines
   - Familiarize yourself with all 5 phase commands

2. **Confirm User Requirements**
   ```
   "I've loaded the 5-phase scientific article analysis protocol. This will:
   - Phase 1: Extract and process the PDF content
   - Phase 2: Analyze citations and research background
   - Phase 3: Perform preliminary analysis with key concepts
   - Phase 4: Conduct deep sectional analysis
   - Phase 5: Create general audience article and professional documents
   
   Please provide:
   - Path to the PDF file to analyze
   - Any specific preferences for the analysis
   - Desired output formats (the system defaults to PDF + DOCX)
   ```

3. **Begin Interactive Execution**
   ```
   "Starting Phase 1: Article Ingestion & Initial Processing
   I'll now read the phase1_ingestion.md command and execute it step by step..."
   ```

### Interactive Phase Management
For each phase:
- **Start** by reading the corresponding phase*.md file
- **Execute** all steps according to the command specifications
- **Apply** the core principles (systematic approach, ULTRATHINK, documentation)
- **Present** results and ask for user validation
- **Wait** for approval before proceeding to next phase

### User Communication Pattern
- **Be transparent** about what you're doing in each step
- **Execute tools automatically** (Gemini CLI, MDConverter, etc.) without asking permission
- **Show results** clearly and ask for validation of outcomes
- **Explain decisions** made during execution
- **Highlight any limitations** or issues encountered
- **Give users control** over strategic decisions and pacing

### Automatic vs. Manual Approval
**Execute Automatically (No User Approval Needed):**
- Gemini CLI commands (`gemini -p "@file.pdf ..."`)
- MDConverter tool usage (`python mdconvert.py ...`)
- File creation and directory setup
- PDF extraction and processing
- Citation searches and downloads
- Document conversion and formatting

**Require User Validation:**
- Processing strategy selection (Full/Strategic/Focused)
- Phase completion and quality assessment
- Final content approval before next phase
- Document formatting preset choices
- Overall workflow direction and modifications

The orchestrator maintains the systematic, high-quality approach of the original protocol while providing the modularity and tool integration needed for flexible, collaborative execution between Claude Code and the user.