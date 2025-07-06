# Claude Tools & Capabilities Documentation

This document outlines the available tools and capabilities for the Scientific Article Analysis & General Audience Communication Protocol.

## PDF Processing Tools

### Primary PDF Processing (Recommended)
- **Gemini CLI**: Superior PDF analysis with comprehensive extraction capabilities
  ```bash
  # Complete PDF processing with text, structure, and metadata
  gemini --yolo -p "@document.pdf Please extract the full text content and store it to a file labeled article_text.txt in the Working_Docs/phase1_ingestion/ directory. Identify the basic structure (like title, abstract, and sections) and store them in article_structure.json"
  
  # Extract embedded images with context
  gemini --yolo -p "@document.pdf Please extract the embedded images and store them in the Working_Docs/phase1_ingestion/figures_extracted/ directory. Create an index of each image file, its location in the document, and surrounding context in figures_inventory.json"
  
  # Extract metadata comprehensively
  gemini --yolo -p "@document.pdf Extract all bibliographic information (authors, journal, publication date, keywords, DOI, abstract) and save as metadata.json"
  ```

### Backup PDF Processing Tools
- **pdftotext**: Extract plain text from PDF files (use if Gemini CLI unavailable)
  ```bash
  pdftotext input.pdf output.txt
  ```
- **pdfplumber**: Python library for detailed PDF text extraction (use if Gemini CLI unavailable)
  ```python
  import pdfplumber
  with pdfplumber.open("document.pdf") as pdf:
      text = "\n".join([page.extract_text() for page in pdf.pages])
  ```
- **pdfimages**: Extract all images from PDF (use if Gemini CLI unavailable)
  ```bash
  pdfimages input.pdf output_prefix
  # Extracts as: output_prefix-000.ppm, output_prefix-001.jpg, etc.
  ```
- **pdf2image**: Convert PDF pages to images (use if Gemini CLI unavailable)
  ```bash
  pdftoppm input.pdf output_prefix -png
  ```
- **pdftotext -layout**: Preserve layout during text extraction (use if Gemini CLI unavailable)
  ```bash
  pdftotext -layout input.pdf output.txt
  ```

## Document Conversion Tools

### Primary Document Conversion (Recommended)
- **MDConverter Tool**: Professional markdown conversion with Eisvogel templates
  ```bash
  # Academic paper with serif fonts and formal layout
  python Tools/mdconverter/mdconvert.py article.md --preset academic-serif
  
  # Modern technical document with sans-serif fonts
  python Tools/mdconverter/mdconvert.py readme.md --preset modern-sans
  
  # Business report with professional styling
  python Tools/mdconverter/mdconvert.py proposal.md --preset business-report
  
  # Multi-column newsletter style
  python Tools/mdconverter/mdconvert.py newsletter.md --preset multi-column
  
  # Convert to Word format
  python Tools/mdconverter/mdconvert.py document.md --format docx --preset academic-serif
  
  # Convert to HTML
  python Tools/mdconverter/mdconvert.py document.md --format html
  ```

#### Available MDConverter Presets
- **academic-serif**: Clean academic style with serif fonts and formal layout
- **modern-sans**: Modern sans-serif design for technical documents  
- **business-report**: Professional business style with headers and corporate layout
- **multi-column**: Multi-column newsletter/magazine style layout (sans-serif)
- **multi-column-serif**: Multi-column newsletter/magazine style layout (serif)

#### MDConverter Requirements
- **Pandoc**: Must be installed separately
  - macOS: `brew install pandoc`
  - Ubuntu/Debian: `sudo apt install pandoc`
- **XeLaTeX**: Required for PDF generation
  - macOS: `brew install --cask mactex`
  - Ubuntu/Debian: `sudo apt install texlive-xetex texlive-fonts-recommended`

### Backup Document Conversion Tools
- **pandoc**: Universal document converter (use if MDConverter unavailable)
  ```bash
  pandoc input.md -o output.docx
  # With custom styling:
  pandoc input.md --reference-doc=template.docx -o output.docx
  ```
- **pandoc**: Markdown to HTML (use if MDConverter unavailable)
  ```bash
  pandoc input.md -o output.html
  # With CSS styling:
  pandoc input.md -c styles.css -o output.html
  ```
- **pandoc**: Academic document generation (use if MDConverter unavailable)
  ```bash
  pandoc input.md -o output.pdf --pdf-engine=xelatex
  ```

## Image Processing Tools

### Format Conversion
- **ImageMagick (convert)**: Convert between image formats
  ```bash
  convert input.ppm output.jpg
  convert input.png -quality 85 output.jpg
  ```

### Image Analysis
- **identify**: Get image information
  ```bash
  identify image.jpg
  # Output: image.jpg JPEG 1024x768 1024x768+0+0 8-bit sRGB 156KB
  ```

### Batch Processing
- **mogrify**: Batch image processing
  ```bash
  mogrify -format jpg *.ppm
  mogrify -resize 50% *.jpg
  ```

## File Management Tools

### Directory Operations
- **mkdir**: Create directory structures
  ```bash
  mkdir -p Working_Docs/{phase1_ingestion,phase2_citations,phase3_preliminary,phase4_analysis,phase5_synthesis,process_logs}
  ```

### File Organization
- **find**: Locate files by criteria
  ```bash
  find . -name "*.pdf" -type f
  find Working_Docs -name "*summary*" -type f
  ```

### Archive Creation
- **tar**: Create archives of completed work
  ```bash
  tar -czf analysis_backup.tar.gz Working_Docs/
  ```

## Research & Analysis Tools

### Citation Search
- **Web Search APIs**: For finding citations
  - Google Scholar API
  - PubMed API
  - Crossref API
  - DOI resolution services

### Text Analysis
- **grep/ripgrep**: Search text patterns
  ```bash
  grep -n "specific term" article_text.txt
  rg "pattern" --type md Working_Docs/
  ```

### JSON Processing
- **jq**: Process JSON data
  ```bash
  jq '.citations[] | select(.category=="foundational")' citations_index.json
  ```

## Quality Assurance Tools

### Spell Checking
- **aspell**: Check spelling in documents
  ```bash
  aspell check document.md
  ```

### Word Count
- **wc**: Count words, lines, characters
  ```bash
  wc -w article.md
  wc -l article_text.txt
  ```

### Validation
- **jsonlint**: Validate JSON files
  ```bash
  jsonlint citations_index.json
  ```

## AI Analysis Tools

### Claude Code Integration
- **Task agents**: For complex analysis tasks
- **Multi-tool coordination**: Batch processing capabilities
- **File analysis**: Reading and processing multiple file types

### Gemini CLI
- **Large Context Analysis**: Leverage Google Gemini's massive context window for analyzing large documents and codebases
- **PDF Processing**: Direct PDF analysis with text extraction and figure interpretation
- **Backup Research**: Use when standard research methods are insufficient
- **Multi-file Analysis**: Process entire directories or multiple files simultaneously

#### Key Gemini CLI Commands
```bash
# PDF text extraction and structure analysis
gemini --yolo -p "@document.pdf Please extract the full text content and store it to a file labeled document.txt in the textextraction/ directory. Identify the basic structure (like title, abstract, and sections) and store them in a .json file"

# Extract embedded images from PDF
gemini --yolo -p "@document.pdf Please extract the embedded images and store them in the embeddedimages/ directory. Create an index of each image file, its location in the document, and surrounding context."

# Figure interpretation and analysis
gemini -p "@document.pdf Describe what Figure 3 in the document illustrates. What features is it highlighting, and what does the caption say about its significance?"

# Section-specific analysis
gemini --yolo -p "@document.pdf Provide a comprehensive analysis of the 'Methods' section and save it to Working_Docs/phase4_analysis/section_analysis_methods.md"

# Key concept extraction
gemini --yolo -p "@document.pdf Extract the key technical terms and their definitions discussed in the paper and save them as a JSON object in Working_Docs/phase3_preliminary/key_concepts.json"

# Citation and reference analysis
gemini --yolo -p "@document.pdf Extract all citations from the References section and format them as JSON with DOI information where available"

# Knowledge gap identification
gemini -p "@document.pdf List all the knowledge gaps or areas for future research mentioned in the conclusion and discussion sections"

# Backup research capabilities
gemini -p "Perform a web search for recent review articles (published since 2020) on [research topic]"
gemini -p "Search for articles that discuss this research to see how it was received in the scientific community"

# Multi-file analysis
gemini -p "@Working_Docs/phase1_ingestion/ @Working_Docs/phase2_citations/ Analyze the relationship between the extracted content and citation research"

# Directory-wide analysis
gemini --all_files -p "Analyze the entire project structure and provide recommendations for improving the analysis workflow"
```

#### When to Use Gemini CLI
- **Large document analysis**: Files >100KB or complex PDFs
- **Context overflow**: When Claude's context window is insufficient
- **PDF processing**: Direct PDF analysis without pre-extraction
- **Multi-file comparison**: Analyzing relationships across multiple files
- **Backup research**: When standard research methods fail
- **Figure interpretation**: Understanding visual content in PDFs
- **Comprehensive extraction**: Getting all content from complex documents

#### Gemini CLI Integration Notes
- Use `@` syntax for file/directory inclusion relative to current working directory
- Excellent for Phase 1 PDF processing and extraction
- Valuable for Phase 2 backup research when citations are unavailable
- Useful for Phase 3-4 when analyzing large sections or multiple files
- Can supplement any phase where context limits are reached

## Environment Setup

### Python Dependencies
```bash
pip install pdfplumber pandas requests beautifulsoup4 numpy
```

### System Dependencies (macOS)
```bash
brew install poppler imagemagick pandoc
# For MDConverter PDF generation:
brew install --cask mactex
```

### System Dependencies (Linux)
```bash
sudo apt-get install poppler-utils imagemagick pandoc
# For MDConverter PDF generation:
sudo apt install texlive-xetex texlive-fonts-recommended
```

## Best Practices

### File Naming Conventions
- Use descriptive names with phase prefixes
- Include date stamps for versions: `analysis_2024-01-15.md`
- Use consistent separators: underscores for files, hyphens for directories

### Directory Structure
```
Working_Docs/
├── phase1_ingestion/
│   ├── figures_extracted/
│   ├── article_text.txt
│   ├── article_structure.json
│   ├── metadata.json
│   └── figures_inventory.json
├── phase2_citations/
│   ├── downloaded_articles/
│   ├── user_provided_articles/
│   ├── citations_index.json
│   ├── search_log.json
│   └── unavailable_articles_report.md
├── phase3_preliminary/
├── phase4_analysis/
├── phase5_synthesis/
└── process_logs/
```

### Quality Control
- Always verify extracted text quality
- Check image extraction completeness
- Validate JSON file formatting
- Test document conversions before finalizing
- Maintain backup copies of all work

### Error Handling
- Document all tool failures and workarounds
- Provide alternative approaches for each tool
- Test tools before starting major processing
- Keep logs of all processing steps

## Tool Selection Guidelines

### For PDF Processing
1. **Primary method**: Use `gemini -p "@document.pdf"` for comprehensive analysis (RECOMMENDED)
2. **Backup text extraction**: Use `pdftotext` if Gemini CLI unavailable
3. **Backup layout preservation**: Use `pdfplumber` if Gemini CLI unavailable
4. **Backup image extraction**: Use `pdfimages` if Gemini CLI unavailable
5. **All PDF tasks**: Default to Gemini CLI first, fall back to traditional tools only if needed

### For Document Conversion
1. **Primary method**: Use `python Tools/mdconverter/mdconvert.py` with appropriate preset (RECOMMENDED)
2. **Academic papers**: Use `--preset academic-serif` for professional academic formatting
3. **Technical docs**: Use `--preset modern-sans` for clean modern styling
4. **Business reports**: Use `--preset business-report` for corporate formatting
5. **Backup conversion**: Use `pandoc` directly if MDConverter unavailable

### For Image Processing
1. **Format conversion**: Use `ImageMagick convert`
2. **Batch processing**: Use `mogrify`
3. **Analysis**: Use `identify`

### For Research
1. **Citation search**: Use multiple APIs and sources
2. **Text analysis**: Use `ripgrep` for speed, `grep` for compatibility
3. **Data processing**: Use `jq` for JSON, `pandas` for complex analysis
4. **Backup research**: Use `gemini -p "search for..."` when standard methods fail
5. **Large document analysis**: Use `gemini -p "@file.pdf"` for comprehensive review

## Troubleshooting

### Common Issues
- **PDF extraction fails**: Try alternative tools or different parameters
- **Images won't convert**: Check ImageMagick policy files
- **Pandoc errors**: Verify template compatibility and dependencies
- **Permission errors**: Check file/directory permissions

### Recovery Strategies
- Always maintain multiple extraction attempts
- Keep original files unchanged
- Document successful parameter combinations
- Create checkpoint saves at each phase

## Integration Notes

These tools integrate with the 5-phase analysis protocol:

- **Phase 1**: PDF processing and image extraction tools
- **Phase 2**: Research and citation tools
- **Phase 3**: Text analysis and processing tools
- **Phase 4**: Advanced analysis and synthesis tools
- **Phase 5**: Document conversion and formatting tools

Each phase command file references the appropriate tools from this documentation.