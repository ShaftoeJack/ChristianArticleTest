# Phase 1: Article Ingestion & Initial Processing

## Command Overview
Extract and parse scientific article content, identify document structure, extract figures, and create foundational files for subsequent analysis phases.

## Input Requirements
- **PDF File**: Scientific article to be processed
- **Working Directory**: `Working_Docs/` structure must exist

## Dependencies
- None (this is the first phase)

## Objectives
- Extract and parse the scientific article content
- Identify document structure and organization
- Extract figures and visual content
- Create foundational temporary files for subsequent phases

## Processing Steps

### 1.1 PDF Text Extraction
- **Action**: Extract raw text from PDF using fastest reliable method with quality validation
- **Primary Tool (RECOMMENDED)**: pdftotext for speed and reliability:
  ```bash
  # Primary extraction method
  pdftotext document.pdf Working_Docs/phase1_ingestion/article_text.txt
  
  # Alternative with layout preservation
  pdftotext -layout document.pdf Working_Docs/phase1_ingestion/article_text.txt
  ```

- **Quality Check Process** (CRITICAL):
  1. **Length Validation**: Check extracted text has >1000 words for typical academic papers
     ```bash
     wc -w Working_Docs/phase1_ingestion/article_text.txt
     ```
  2. **Content Validation**: Verify first ~50 lines contain:
     - Document title matching filename
     - Author names and affiliations
     - Abstract or introduction text
     - Proper sentence structure (not garbled OCR)
  3. **Assessment Criteria**:
     - **PASS**: Text length appropriate, title/authors visible, readable sentences
     - **FAIL**: Very short text, no recognizable title/authors, mostly symbols/garbled text

- **Fallback for Non-OCR PDFs**: If quality check fails, use Gemini CLI for OCR extraction:
  ```bash
  gemini --yolo -p "@document.pdf This PDF may not be OCR'd. Please extract the full text content using OCR capabilities and store it to Working_Docs/phase1_ingestion/article_text.txt"
  ```

- **Output**: `Working_Docs/phase1_ingestion/article_text.txt`
- **Documentation**: Record extraction method used (pdftotext/Gemini OCR), quality check results, any issues encountered

### 1.2 Document Structure Analysis
- **Action**: Identify and map article sections (Abstract, Introduction, Methods, Results, Discussion, Conclusion, References)
- **Primary Tool (RECOMMENDED)**: Gemini CLI for comprehensive structure analysis:
  ```bash
  gemini --yolo -p "@document.pdf Identify the basic structure (like title, abstract, and sections) and store them in Working_Docs/phase1_ingestion/article_structure.json file"
  ```
- **Backup Method**: Manual analysis of extracted text file if Gemini CLI unavailable
- **Output**: `Working_Docs/phase1_ingestion/article_structure.json`
- **Format**:
```json
{
  "title": "Article Title",
  "sections": [
    {"name": "Abstract", "start_line": 1, "end_line": 15},
    {"name": "Introduction", "start_line": 16, "end_line": 45}
  ],
  "figures": ["Figure 1: Description", "Figure 2: Description"],
  "tables": ["Table 1: Description"]
}
```

### 1.3 Metadata Extraction
- **Action**: Extract bibliographic and descriptive information
- **Primary Tool (RECOMMENDED)**: Gemini CLI for comprehensive metadata extraction:
  ```bash
  gemini --yolo -p "@document.pdf Extract all bibliographic information (authors, journal, publication date, keywords, DOI, abstract) and save as Working_Docs/phase1_ingestion/metadata.json"
  ```
- **Backup Method**: Manual extraction from text file if Gemini CLI unavailable
- **Output**: `Working_Docs/phase1_ingestion/metadata.json`
- **Include**: Authors, journal, publication date, keywords, DOI, abstract, key terms

### 1.4 Figure Extraction and Inventory
- **Action**: Extract all figures/images from PDF with contextual analysis
- **Primary Tool (RECOMMENDED)**: Gemini CLI for superior figure extraction and analysis:
  ```bash
  gemini --yolo -p "@document.pdf Please extract the embedded images and store them in the Working_Docs/phase1_ingestion/figures_extracted/ directory. Create an index of each image file, its location in the document, and surrounding context in Working_Docs/phase1_ingestion/figures_inventory.json"
  ```
- **Backup Method**: If Gemini CLI unavailable, use traditional tools:
  ```bash
  # Create directory first
  mkdir -p Working_Docs/phase1_ingestion/figures_extracted/
  
  # Extract images
  pdfimages document.pdf Working_Docs/phase1_ingestion/figures_extracted/figure
  ```
- **Output**: 
  - `Working_Docs/phase1_ingestion/figures_extracted/` directory with all images
  - `Working_Docs/phase1_ingestion/figures_inventory.json` with metadata
- **Inventory Format**:
```json
{
  "total_extracted": "N",
  "extraction_method": "pdfimages",
  "figures": [
    {
      "file": "figure-XXX.ppm",
      "size_kb": "XXX",
      "dimensions": "widthxheight",
      "likely_content": "Scientific figure vs header/logo",
      "priority": "high/medium/low"
    }
  ]
}
```
- **Documentation**: Record extraction success rate, file formats, resolution quality

### 1.5 Quality Check and Article Length Assessment
- **Verify**: Text extraction completeness, structure identification accuracy
- **Assess**: Article length and complexity for processing strategy selection
- **Strategy Selection**:
  - **Small** (<8,000 words): Standard processing, read full sections directly
  - **Medium** (8,000-20,000 words): Strategic processing, use Task agents for large sections
  - **Large** (>20,000 words): Focused processing, sample key sections, extensive use of Task agents
- **Document**: Any missing sections, extraction issues, or quality concerns
- **Output**: `Working_Docs/process_logs/phase1_log.md`

## Quality Assurance Checkpoints
Before proceeding to next phase:
- [ ] All required outputs created and properly formatted
- [ ] Process documentation complete and transparent
- [ ] Quality standards met (accuracy, completeness, integration)
- [ ] Prerequisites for next phase established
- [ ] Knowledge gaps and limitations clearly documented

## Output Files
- `Working_Docs/phase1_ingestion/article_text.txt` - Raw extracted text
- `Working_Docs/phase1_ingestion/article_structure.json` - Document structure map
- `Working_Docs/phase1_ingestion/metadata.json` - Bibliographic information
- `Working_Docs/phase1_ingestion/figures_extracted/` - Directory of extracted images
- `Working_Docs/phase1_ingestion/figures_inventory.json` - Figure metadata
- `Working_Docs/process_logs/phase1_log.md` - Process documentation

## Success Criteria
- Text extraction >95% complete
- All major sections identified
- Figure extraction successful
- Metadata completely captured
- Processing strategy determined
- Quality documentation complete

## Error Handling
- If Gemini CLI fails, fall back to traditional PDF tools (pdftotext, pdfimages)
- If traditional PDF extraction fails, try alternative parameters or tools
- If figures cannot be extracted, document limitation and proceed with available content
- If structure cannot be identified, proceed with manual section marking
- Always document issues and workarounds
- Gemini CLI should be attempted first for all PDF processing tasks

## Next Phase Prerequisites
- All output files created
- Article length and complexity assessed
- Processing strategy determined
- Quality checkpoints passed