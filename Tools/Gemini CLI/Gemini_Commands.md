 # Using Gemini CLI for Large Codebase Analysis

  When analyzing large documents or multiple files that might exceed context limits, use the Gemini CLI with its massive context window. In addition, use Gemini CLI to ingest and process pdfs.  Also use Gemini CLI for backup research when your research has not returned useful results.  
  
  ## Rules
  The way to call Gemini CLI is to make a bash call as shown in the examples below.  
  - Requests only requiring a text response: gemini -p "[Instruction to return an answer]"  
  - Requests to create a file: gemini --yolo -p "[Instruction to return and answer and create files]".  
  
  Use "--yolo" flag carefully.  With it Gemini CLI has access to Bash.  If you need Gemini to write a file to a folder, make sure you create the folder first and direct Gemini to work on that existing folder.

  ## File and Directory Inclusion Syntax

  Use the `@` syntax to include files and directories in your Gemini prompts. The paths should be relative to WHERE you run the gemini command:

    ### Examples:

    - Single file analysis **no file writing**: 
      * gemini -p "@src/main.py Explain this file's purpose and structure"

    - Multiple files **no file writing**: 
      * gemini -p "@package.json @src/index.js Analyze the dependencies used in the code"

    - Entire directory **no file writing**: 
      * gemini -p "@src/ Summarize the architecture of this codebase"

    - Multiple directories **no file writing**: 
      * gemini -p "@src/ @tests/ Analyze test coverage for the source code"

    - Current directory and subdirectories **no file writing**: 
      * gemini -p "@./ Give me an overview of this entire project"
    
    - use --all_files flag **no file writing**: 
      * gemini --all_files -p "Analyze the project structure and dependencies"

  ## PDF Processing

    - Extract text from a pdf **file writing**:  
      * gemini --yolo -p "@document.pdf Please extract the full text content and store it to a file labeled @document.txt in the @textextraction/ directory.  Identify the basic structure (like title, abstract, and sections) and store them in a .json file"

    - Extract embedded images from a pdf **file writing**:  
      * gemini --yolo -p "@document.pdf Please extract the embedded images and store them in the @embeddedimages/ directory.  Create an index of each image file, its location in the document, and surrounding context in the document."
    
    - Figure and Image Interpretation **no file writing**:
      * gemini -p "@document.pdfDescribe what Figure 3 in the document illustrates.  What anatomical features is it highlighting, and what does the caption say about its significance?"

    - General and specific summaries **file writing**: 
      * gemini --yolo -p "@document.pdf Provide a one-paragraph executive summary of the Galesaurus planiceps paper and save it to @Working_Docs/phase5_synthesis/executive_summary.md. Summarize only the 'Discussion' section of the paper."

    - Ask specific questions about the document: 
      * gemini -p "What was the primary hypothesis of the study regarding Galesaurus planiceps?"
      * gemini --yolo -p "@document.pdf Extract the key anatomical terms and their definitions discussed in the paper and save them as a JSON object in @Working_Docs/phase3_preliminary/key_concepts.json."
      * gemini -p "@document.pdf List all the knowledge gaps or areas for future research mentioned in the conclusion."

## Additional Research
    - Backup research:
      * gemini -p "Perform a web search for recent review articles (published since 2020) on early cynodont evolution."
      * gemini -p "Who are the key authors publishing research on Triassic-period therapsids? Search for their university affiliations or most cited works."
 
    - Gathering Context and Related Work:
      * gemini -p "Search for articles or blog posts that discuss the 2019 Pusch et al. paper on Galesaurus planiceps to see how it was received in the scientific community."

    - Comparing Information Across Multiple Sources:
      * gemini -p "Please fetch the information from these three URLs on cynodont diets:
        1. [URL 1]
        2. [URL 2]
        3. [URL 3]
      Compare the information and provide a summary of the different hypotheses regarding what early cynodonts ate.

# When to Use Gemini CLI

  Use gemini -p when:
  - Analyzing large files or large directories
  - Comparing multiple large files
  - Need to understand patterns across multiple files
  - Current context window is insufficient for the task
  - Working with files totaling more than 100KB
  - Verifying if specific features, patterns, or security measures are implemented
  - For research when your research has not been successful.

  Important Notes

  - Paths in @ syntax are relative to your current working directory when invoking gemini
  - The CLI will include file contents directly in the context
  - Gemini's context window can handle entire codebases and large folder structures that would overflow Claude's context
  - When checking implementations, be specific about what you're looking for to get accurate results 