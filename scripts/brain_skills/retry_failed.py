import os
import re
from pathlib import Path
import extract_pdf
import summarize_text

WIKI_DIR = Path(__file__).parent.parent.parent / "wiki"
RAW_DIR = Path(__file__).parent.parent.parent / "raw"
FAILED_PATH = WIKI_DIR / "failed_ingestions.md"
IGNORED_PATH = WIKI_DIR / "ignored_readings.md"

def retry_failed_ingestions():
    if not FAILED_PATH.exists():
        print("No failed_ingestions.md file found.")
        return

    content = FAILED_PATH.read_text(encoding="utf-8")
    
    # We will look for blocks like:
    # - **Reading:** Some Text
    #   - **Reason:** Some reason
    #   - **Manual PDF Path:** C:\path\to\file.pdf
    
    blocks = content.split("- **Reading:** ")
    if len(blocks) <= 1:
        print("No failed readings to process.")
        return
        
    header = blocks[0]
    new_blocks = [header]
    
    processed_any = False

    for block in blocks[1:]:
        lines = block.split('\n')
        reading_text = lines[0].strip()
        
        # Skip if already resolved or ignored
        if reading_text.endswith("[RESOLVED]") or reading_text.endswith("[IGNORED]"):
            processed_any = True
            continue
            
        path_line_idx = -1
        pdf_path = ""
        for i, line in enumerate(lines):
            if line.strip().startswith("- **Manual PDF Path:**"):
                path_line_idx = i
                pdf_path = line.split("**Manual PDF Path:**")[1].strip()
                break
                
        if not pdf_path:
            new_blocks.append("- **Reading:** " + block.strip() + "\n\n")
            continue
            
        # Strip quotes if user added them
        pdf_path = pdf_path.strip('"').strip("'")
        
        if pdf_path.upper() == "IGNORE":
            print(f"\nIgnoring: {reading_text[:50]}...")
            
            # Save to ignored_readings.md
            with open(IGNORED_PATH, "a", encoding="utf-8") as f:
                f.write(f"{reading_text}\n")
                
            processed_any = True
            continue

        if not os.path.exists(pdf_path):
            print(f"Warning: Path does not exist for '{reading_text[:30]}...': {pdf_path}")
            new_blocks.append("- **Reading:** " + block.strip() + "\n\n")
            continue
            
        print(f"\nProcessing Manual Path for: {reading_text[:50]}...")
        
        RAW_DIR.mkdir(exist_ok=True)
        
        # Extract title clue from reading text
        title_match = re.search(r'"([^"]+)"', reading_text)
        title_clue = title_match.group(1) if title_match else reading_text[:30]
        safe_title = "".join(c for c in title_clue if c.isalnum() or c in (' ', '_')).replace(' ', '_').strip()
        
        raw_path = RAW_DIR / f"{safe_title}_manual.txt"
        wiki_path = WIKI_DIR / "summaries" / f"summary_{safe_title}_manual.md"
        
        try:
            # Look for page ranges in the reading_text to extract selectively
            start_page = None
            end_page = None
            page_match = re.search(r'pp\s*(\d+)\s*-\s*(\d+)', reading_text, re.IGNORECASE)
            
            # If we don't find it there, check if the user provided it in the path string e.g. "path.pdf [87-100]"
            if not page_match:
                page_match = re.search(r'\[(\d+)\s*-\s*(\d+)\]', pdf_path)
                if page_match:
                    pdf_path = re.sub(r'\s*\[(\d+)\s*-\s*(\d+)\]', '', pdf_path).strip()
            
            if page_match:
                # Add a 15 page buffer to account for preface numbering offsets
                start_page = max(0, int(page_match.group(1)) - 15)
                end_page = int(page_match.group(2)) + 15
                print(f"  -> Detected page range. Extracting pages {start_page} to {end_page} from {os.path.basename(pdf_path)}...")
            else:
                print(f"  -> Extracting full text from {os.path.basename(pdf_path)}...")
                
            raw_text = extract_pdf.extract_text(pdf_path, start_page, end_page)
            raw_path.write_text(raw_text, encoding="utf-8")
            
            print("  -> Generating AI Summary...")
            # We don't have the module name here easily, so we just say "Manual Retry"
            metadata = {'module': 'Manual Retry', 'assigned': 'true', 'student_presentation': 'false'}
            summary = summarize_text.generate_wiki_summary(raw_text, title_clue, "Manual PDF", metadata)
            
            if summary:
                wiki_path.write_text(summary, encoding="utf-8")
                summarize_text.update_wiki_log(f"Manual retry ingested: {title_clue}")
                summarize_text.update_wiki_index("Paper Summaries", f"[{title_clue}](summaries/{wiki_path.name}) - Resolved")
                print("  -> Success!")
                
                # Successfully resolved, so omit it from new_blocks
                processed_any = True
            else:
                print("  -> Failed to generate summary.")
                new_blocks.append("- **Reading:** " + block.strip() + "\n\n")
        except Exception as e:
            print(f"  -> Error: {e}")
            new_blocks.append("- **Reading:** " + block.strip() + "\n\n")

    if processed_any:
        # Save updated failed_ingestions.md
        new_content = "".join(new_blocks)
        FAILED_PATH.write_text(new_content, encoding="utf-8")
        print("\nUpdated failed_ingestions.md with [RESOLVED] tags.")
    else:
        print("\nNo valid new paths found to process.")

if __name__ == "__main__":
    retry_failed_ingestions()
