# MD Converter Tool - Eisvogel Edition

A simple, robust markdown-to-document converter using the professional Eisvogel template with preset configurations optimized for Claude Code integration.

## Overview

This tool converts Markdown files to PDF, DOCX, or HTML using the renowned Eisvogel LaTeX template. It includes 4 carefully crafted preset configurations that handle all the complex template variables automatically.

## Requirements

- Python 3.7+
- Pandoc (must be installed separately)
  - macOS: `brew install pandoc` 
  - Ubuntu/Debian: `sudo apt install pandoc`
  - Windows: Download from https://pandoc.org/installing.html
- XeLaTeX (for PDF generation)
  - macOS: `brew install --cask mactex`
  - Ubuntu/Debian: `sudo apt install texlive-xetex texlive-fonts-recommended`

## Quick Start

```bash
# Download the Eisvogel template (automatic on first use)
uv run python mdconvert.py --download-template

# List available presets
uv run python mdconvert.py --list-presets

# Convert with academic styling
uv run python mdconvert.py document.md --preset academic-serif

# Convert with modern sans-serif design
uv run python mdconvert.py document.md --preset modern-sans
```

## Available Presets

### 1. **academic-serif** 🎓
- **Best for**: Academic papers, research documents, theses
- **Features**: 12pt Libertinus serif fonts, 1.5 line spacing, formal TOC, numbered sections
- **Style**: Clean, traditional academic formatting with blue links

### 2. **modern-sans** 💻  
- **Best for**: Technical documentation, README files, modern reports
- **Features**: 11pt Lato sans-serif fonts, 1.4 line spacing, clean design
- **Style**: Modern, technical look with smaller code blocks

### 3. **business-report** 💼
- **Best for**: Business proposals, corporate reports, professional documents
- **Features**: Title page, professional headers/footers, 11pt fonts, extra top margin
- **Style**: Corporate styling with date stamps and page numbers

### 4. **multi-column** 📰
- **Best for**: Newsletters, magazines, brochures, informational sheets
- **Features**: 2-column layout, 10pt fonts, colored table rows, compact design
- **Style**: Magazine-style layout with efficient space usage

## Command Line Usage

```bash
# Basic conversion (defaults to PDF with no preset)
uv run python mdconvert.py input.md

# Specify format and preset
uv run python mdconvert.py input.md --format pdf --preset academic-serif

# Convert to Word document
uv run python mdconvert.py input.md --format docx --preset business-report

# Custom output filename
uv run python mdconvert.py input.md --preset modern-sans --output final_report.pdf
```

## Complete Command Reference

### Required Arguments
- `input`: Path to the markdown file to convert

### Optional Arguments
- `-f, --format`: Output format (`pdf`, `docx`, `doc`, `html`) - default: `pdf`
- `-p, --preset`: Eisvogel preset (`academic-serif`, `modern-sans`, `business-report`, `multi-column`)
- `-o, --output`: Output file path (default: auto-generated from input name)

### Utility Commands
- `--list-presets`: Show all available presets with descriptions
- `--download-template`: Download/update the Eisvogel template
- `-h, --help`: Show help message with examples

## Examples for Claude Code

When helping users convert markdown files, use these exact patterns:

```bash
# Academic paper conversion
uv run python mdconvert.py research_paper.md --preset academic-serif

# Technical documentation  
uv run python mdconvert.py api_docs.md --preset modern-sans

# Business proposal
uv run python mdconvert.py proposal.md --preset business-report --format pdf

# Newsletter/magazine style
uv run python mdconvert.py newsletter.md --preset multi-column

# Convert to Word for collaboration
uv run python mdconvert.py draft.md --preset academic-serif --format docx

# HTML for web publishing
uv run python mdconvert.py article.md --format html
```

## Preset Configuration Details

Each preset automatically configures these Eisvogel template variables:

### Academic Serif Variables
```
fontfamily: libertinus, fontsize: 12pt, geometry: margin=1in
linestretch: 1.5, toc: true, toc-own-page: true
number-sections: true, colorlinks: true, linkcolor: blue
```

### Modern Sans Variables  
```
fontfamily: lato, fontfamilyoptions: default,defaultsans
fontsize: 11pt, geometry: margin=0.8in, linestretch: 1.4
code-block-font-size: \footnotesize, linkcolor: black
```

### Business Report Variables
```
fontfamily: libertinus, fontsize: 11pt, geometry: margin=1in,top=1.5in
titlepage: true, header-right: \thepage, footer-right: \today
linestretch: 1.2, titlepage-color: FFFFFF
```

### Multi-column Variables
```
fontfamily: libertinus, fontsize: 10pt, geometry: margin=0.75in
toc: false, number-sections: false, table-use-row-colors: true
code-block-font-size: \scriptsize + multicol environment
```

## Automatic Features

- **Template Download**: Eisvogel template downloads automatically on first use
- **Font Fallbacks**: If specified fonts aren't available, LaTeX will use system defaults
- **Error Handling**: Clear error messages for missing files, Pandoc issues, etc.
- **Cross-platform**: Works on macOS, Linux, and Windows

## Troubleshooting

### Common Issues
1. **"Pandoc not found"**: Install Pandoc using package manager
2. **"XeLaTeX not found"**: Install full LaTeX distribution (MacTeX, TeX Live)
3. **Font errors**: Template will fall back to system fonts automatically
4. **Template download fails**: Check internet connection, retry with `--download-template`

### Dependencies Check
```bash
# Verify Pandoc installation
pandoc --version

# Verify XeLaTeX installation  
xelatex --version

# Manual template download (if automatic fails)
uv run python mdconvert.py --download-template
```

## Integration Notes

- All presets work with complex markdown including tables, code blocks, images, and math
- Output files are generated in the same directory as input by default
- Templates handle metadata from YAML front matter automatically
- Multi-column preset requires special LaTeX processing (handled automatically)
- HTML output doesn't use Eisvogel template (uses Pandoc defaults)

## File Structure

```
mdconverter/
├── mdconvert.py          # Main CLI script with Eisvogel integration
├── requirements.txt      # Dependencies (minimal - just Python stdlib)
├── templates/           # Auto-created directory
│   └── eisvogel.latex   # Downloaded Eisvogel template
└── MDConverter.md      # This documentation
```

The tool is designed to be completely self-contained - just ensure Pandoc and LaTeX are installed on the system.