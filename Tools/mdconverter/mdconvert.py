#!/usr/bin/env python3
"""
MD Converter - Simple markdown to PDF/DOC converter with Eisvogel templates
"""

import argparse
import os
import sys
import urllib.request
from pathlib import Path
import subprocess
import tempfile

class MDConverter:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.templates_dir = self.script_dir / "templates"
        self.eisvogel_template = self.templates_dir / "eisvogel.tex"
        self.supported_formats = ['pdf', 'docx', 'doc', 'html']
        self.available_presets = ['academic-serif', 'modern-sans', 'business-report', 'multi-column', 'multi-column-serif']
        
        # Ensure templates directory exists
        self.templates_dir.mkdir(exist_ok=True)
    
    def check_pandoc(self):
        """Check if pandoc is installed"""
        try:
            result = subprocess.run(['pandoc', '--version'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  check=True, text=True)
            return True, result.stdout.split('\n')[0]
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False, "Pandoc not found"
    
    def download_eisvogel_template(self):
        """Download the Eisvogel template if not present"""
        if self.eisvogel_template.exists():
            return True, "Template already exists"
        
        eisvogel_url = "https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template/v2.4.0/eisvogel.tex"
        
        try:
            print("Downloading Eisvogel template...")
            urllib.request.urlretrieve(eisvogel_url, self.eisvogel_template)
            return True, "Template downloaded successfully"
        except Exception as e:
            return False, f"Failed to download template: {str(e)}"
    
    def get_preset_config(self, preset_name):
        """Get configuration for a preset"""
        presets = {
            'academic-serif': {
                'description': 'Clean academic style with serif fonts and formal layout',
                'variables': {
                    'mainfont': 'Georgia',
                    'fontsize': '12pt',
                    'geometry': 'margin=1in',
                    'linestretch': '1.5',
                    'toc': 'true',
                    'toc-own-page': 'true',
                    'number-sections': 'true',
                    'colorlinks': 'true',
                    'linkcolor': 'blue',
                    'citecolor': 'blue'
                }
            },
            'modern-sans': {
                'description': 'Modern sans-serif design for technical documents',
                'variables': {
                    'mainfont': 'Helvetica',
                    'fontsize': '11pt',
                    'geometry': 'margin=0.8in',
                    'linestretch': '1.4',
                    'toc': 'true',
                    'number-sections': 'true',
                    'colorlinks': 'true',
                    'linkcolor': 'black',
                    'code-block-font-size': '\\footnotesize'
                }
            },
            'business-report': {
                'description': 'Professional business style with headers and corporate layout',
                'variables': {
                    'mainfont': 'Georgia',
                    'fontsize': '11pt',
                    'geometry': 'margin=1in,top=1.5in',
                    'linestretch': '1.2',
                    'toc': 'true',
                    'number-sections': 'true',
                    'colorlinks': 'true',
                    'linkcolor': 'blue',
                    'header-right': '\\thepage',
                    'footer-right': '\\today',
                    'titlepage': 'true',
                    'titlepage-color': 'FFFFFF',
                    'titlepage-text-color': '000000'
                }
            },
            'multi-column': {
                'description': 'Multi-column newsletter/magazine style layout (sans-serif)',
                'variables': {
                    'mainfont': 'Helvetica',
                    'fontsize': '10pt',
                    'geometry': 'margin=0.75in',
                    'linestretch': '1.3',
                    'toc': 'false',
                    'number-sections': 'false',
                    'colorlinks': 'true',
                    'linkcolor': 'blue',
                    'code-block-font-size': '\\scriptsize',
                    'table-use-row-colors': 'true'
                }
            },
            'multi-column-serif': {
                'description': 'Multi-column newsletter/magazine style layout (serif)',
                'variables': {
                    'mainfont': 'Georgia',
                    'fontsize': '10pt',
                    'geometry': 'margin=0.75in',
                    'linestretch': '1.3',
                    'toc': 'false',
                    'number-sections': 'false',
                    'colorlinks': 'true',
                    'linkcolor': 'blue',
                    'code-block-font-size': '\\scriptsize',
                    'table-use-row-colors': 'true'
                }
            }
        }
        return presets.get(preset_name)
    
    def convert_document(self, input_file, output_file, format_type, preset_name=None):
        """Convert markdown file to specified format using Eisvogel template"""
        
        # Ensure Eisvogel template is available
        success, message = self.download_eisvogel_template()
        if not success:
            return False, message
        
        # Build pandoc command
        cmd = ['pandoc', str(input_file), '-o', str(output_file)]
        
        # Add format-specific options
        if format_type == 'pdf':
            cmd.extend(['--pdf-engine=xelatex'])
            # Only use Eisvogel template if fonts are available, otherwise use default
            if preset_name:
                cmd.extend(['--template', str(self.eisvogel_template)])
            # Add basic styling for PDF without template
            cmd.extend(['-V', 'geometry:margin=1in'])
        
        # Add preset configuration
        if preset_name and format_type == 'pdf':
            preset_config = self.get_preset_config(preset_name)
            if preset_config:
                for key, value in preset_config['variables'].items():
                    cmd.extend(['--variable', f'{key}={value}'])
        
        # Add some sensible defaults
        cmd.extend([
            '--standalone',
            '--highlight-style=tango',
            '--from=markdown+lists_without_preceding_blankline'
        ])
        
        # For multi-column presets, add special handling
        if preset_name in ['multi-column', 'multi-column-serif'] and format_type == 'pdf':
            # Create temporary file with multicol wrapper
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
                temp_path = temp_file.name
                with open(input_file, 'r') as original:
                    content = original.read()
                
                # Wrap content in multicol environment
                multicol_content = f"""---
header-includes: |
  \\usepackage{{multicol}}
  \\newcommand{{\\hideFromPandoc}}[1]{{#1}}
  \\hideFromPandoc{{
    \\let\\Begin\\begin
    \\let\\End\\end
  }}
---

\\Begin{{multicols}}{{2}}

{content}

\\End{{multicols}}
"""
                temp_file.write(multicol_content)
            
            # Update command to use temporary file
            cmd[1] = temp_path
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Clean up temporary file if created
            if preset_name in ['multi-column', 'multi-column-serif'] and format_type == 'pdf':
                os.unlink(temp_path)
            
            return True, ""
        except subprocess.CalledProcessError as e:
            # Clean up temporary file if created
            if preset_name in ['multi-column', 'multi-column-serif'] and format_type == 'pdf':
                try:
                    os.unlink(temp_path)
                except:
                    pass
            return False, f"Pandoc error: {e.stderr}"
    
    def list_presets(self):
        """List available presets with descriptions"""
        print("Available Eisvogel presets:")
        for preset in self.available_presets:
            config = self.get_preset_config(preset)
            if config:
                print(f"  • {preset:<15} - {config['description']}")

def main():
    parser = argparse.ArgumentParser(
        description='Convert markdown files to PDF, DOC, or HTML using Eisvogel template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Academic paper with serif fonts and formal layout
  python mdconvert.py article.md --preset academic-serif
  
  # Modern technical document with sans-serif fonts  
  python mdconvert.py readme.md --preset modern-sans
  
  # Business report with professional styling
  python mdconvert.py proposal.md --preset business-report --format pdf
  
  # Multi-column newsletter style
  python mdconvert.py newsletter.md --preset multi-column
  
  # Convert to Word format
  python mdconvert.py document.md --format docx --preset academic-serif
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input markdown file')
    parser.add_argument('-f', '--format', 
                       choices=['pdf', 'docx', 'doc', 'html'],
                       default='pdf',
                       help='Output format (default: pdf)')
    parser.add_argument('-p', '--preset',
                       choices=['academic-serif', 'modern-sans', 'business-report', 'multi-column', 'multi-column-serif'],
                       help='Eisvogel preset configuration')
    parser.add_argument('-o', '--output',
                       help='Output file (default: input name with new extension)')
    parser.add_argument('--list-presets', action='store_true',
                       help='List available presets and exit')
    parser.add_argument('--download-template', action='store_true',
                       help='Download/update Eisvogel template and exit')
    
    args = parser.parse_args()
    
    converter = MDConverter()
    
    # Handle preset listing
    if args.list_presets:
        converter.list_presets()
        return 0
    
    # Handle template download
    if args.download_template:
        success, message = converter.download_eisvogel_template()
        print(message)
        return 0 if success else 1
    
    # Validate input file is provided
    if not args.input:
        parser.error("Input file is required (unless using --list-presets or --download-template)")
        return 1
    
    # Check if pandoc is installed
    pandoc_available, pandoc_info = converter.check_pandoc()
    if not pandoc_available:
        print("Error: Pandoc is not installed or not in PATH")
        print("Please install pandoc: https://pandoc.org/installing.html")
        return 1
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found")
        return 1
    
    if not input_path.suffix.lower() in ['.md', '.markdown']:
        print(f"Warning: Input file '{args.input}' doesn't have .md extension")
    
    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        format_ext = 'docx' if args.format == 'doc' else args.format
        output_path = input_path.with_suffix(f'.{format_ext}')
    
    # Convert document
    print(f"Converting '{input_path}' to {args.format.upper()}...")
    if args.preset:
        preset_config = converter.get_preset_config(args.preset)
        print(f"Using preset: {args.preset} - {preset_config['description']}")
    
    success, error_msg = converter.convert_document(
        input_path, output_path, args.format, args.preset
    )
    
    if success:
        print(f"✓ Successfully created: {output_path}")
        return 0
    else:
        print(f"✗ Conversion failed: {error_msg}")
        return 1

if __name__ == '__main__':
    sys.exit(main())