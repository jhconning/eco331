import os
import re
import glob
from pathlib import Path
import extract_pdf
import extract_pptx
import summarize_text

SCHEDULE_PATH = Path(__file__).parent.parent.parent / "canvas" / "canvas_pages" / "course_outline_and_reading_schedule.md"
ZOT_DIR = r"C:\MyGDrive\B\zot_pdfs"
RAW_DIR = Path(__file__).parent.parent.parent / "raw"
WIKI_DIR = Path(__file__).parent.parent.parent / "wiki"
KR_DIR = Path(__file__).parent.parent.parent / "read" / "KRbook"
FAILED_PATH = WIKI_DIR / "failed_ingestions.md"
IGNORED_PATH = WIKI_DIR / "ignored_readings.md"

def find_pdf_fuzzy(title_clue):
    """Attempt to find a PDF in the Zotero directory matching the clue."""
    words = [w.lower() for w in re.findall(r'\w+', title_clue) if len(w) > 3]
    if not words:
        return None
        
    best_match = None
    max_score = 0
    
    for filename in os.listdir(ZOT_DIR):
        if not filename.lower().endswith('.pdf'):
            continue
            
        score = sum(1 for w in words if w in filename.lower())
        if score > max_score and score >= len(words) * 0.5:
            max_score = score
            best_match = os.path.join(ZOT_DIR, filename)
            
    return best_match

def process_special_book(prefix, reading_text, metadata):
    """Handles KR and OG book references."""
    print(f"  -> Detected Special Case: {prefix} Textbook")
    
    # Try to extract a chapter number
    match = re.search(rf"{prefix}\s*(\d+)", reading_text)
    chapter_num = match.group(1) if match else "Unknown"
    
    safe_title = f"{prefix}_Chapter_{chapter_num}"
    wiki_path = WIKI_DIR / "summaries" / f"summary_{safe_title}.md"
    
    if wiki_path.exists():
        print(f"  -> Summary already exists. Skipping.")
        return
        
    summary = None
    
    if prefix == "OG":
        print(f"  -> Using Zero-Shot Generation for Galor Chapter {chapter_num}...")
        prompt_info = f"Oded Galor, 'The Journey of Humanity', Chapter {chapter_num}. Context: {reading_text}"
        summary = summarize_text.generate_zero_shot_summary(prompt_info, metadata)
        
    elif prefix == "KR":
        print(f"  -> Looking for local materials for Koyama & Rubin Chapter {chapter_num}...")
        found_text = None
        
        if KR_DIR.exists():
            for f in os.listdir(KR_DIR):
                if f"Chapter_{chapter_num}" in f or f"Chapter {chapter_num}" in f:
                    file_path = KR_DIR / f
                    print(f"  -> Found local material: {f}")
                    if f.endswith('.pptx'):
                        found_text = extract_pptx.extract_text(str(file_path))
                    elif f.endswith('.md'):
                        found_text = file_path.read_text(encoding='utf-8')
                    break
        
        if found_text:
            print("  -> Generating summary from local teaching materials...")
            raw_path = RAW_DIR / f"{safe_title}_raw.txt"
            raw_path.write_text(found_text, encoding='utf-8')
            summary = summarize_text.generate_wiki_summary(found_text, f"Koyama & Rubin Chapter {chapter_num}", reading_text, metadata)
        else:
            print("  -> No local material found. Falling back to Zero-Shot Generation...")
            prompt_info = f"Mark Koyama and Jared Rubin, 'How the World Became Rich', Chapter {chapter_num}. Context: {reading_text}"
            summary = summarize_text.generate_zero_shot_summary(prompt_info, metadata)

        if summary:
            wiki_path.write_text(summary, encoding="utf-8")
            summarize_text.update_wiki_log(f"Batch ingested special text: {prefix} Chapter {chapter_num}")
            summarize_text.update_wiki_index("Paper Summaries", f"[{prefix} Ch {chapter_num}](summaries/{wiki_path.name}) - Module: {metadata.get('module')}")
            print("  -> Success!")
        else:
            print("  -> Failed to generate summary.")
            summarize_text.update_failed_ingestions(reading_text, f"Failed to generate zero-shot summary for {prefix} chapter {chapter_num}.")


def parse_schedule_and_ingest():
    if not SCHEDULE_PATH.exists():
        print(f"Schedule file not found: {SCHEDULE_PATH}")
        return
        
    content = SCHEDULE_PATH.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    current_module = ""
    
    RAW_DIR.mkdir(exist_ok=True)
    WIKI_DIR.mkdir(exist_ok=True)
    
    # Load ignored readings
    ignored_readings = set()
    if IGNORED_PATH.exists():
        content = IGNORED_PATH.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.strip():
                ignored_readings.add(line.strip())
    
    print("Parsing schedule...")
    for line in lines:
        line = line.strip()
        
        if line.startswith('### '):
            current_module = line[4:].strip()
            
        elif line.startswith('* ') and len(line) > 10:
            reading_text = line[2:].strip()
            
            if reading_text in ignored_readings:
                print(f"\nSkipping Ignored Reading: {reading_text[:50]}...")
                continue
                
            is_presentation = "student presentation" in current_module.lower() or "presentation" in reading_text.lower()
            metadata = {
                'module': current_module,
                'student_presentation': str(is_presentation).lower(),
                'assigned': 'true'
            }
            
            print(f"\nProcessing Reading: {reading_text[:50]}...")
            
            # Check for Special Textbooks
            if reading_text.startswith("KR ") or " KR " in reading_text:
                process_special_book("KR", reading_text, metadata)
                continue
            elif reading_text.startswith("OG ") or " OG " in reading_text or reading_text.startswith("OG,"):
                process_special_book("OG", reading_text, metadata)
                continue
            
            # Standard PDF matching
            title_match = re.search(r'"([^"]+)"', reading_text)
            title_clue = title_match.group(1) if title_match else reading_text[:30]
            
            pdf_path = find_pdf_fuzzy(title_clue)
            if not pdf_path:
                print(f"  -> Could not find matching PDF for clue: '{title_clue}'")
                summarize_text.update_failed_ingestions(reading_text, "Could not find matching PDF locally.")
                continue
                
            print(f"  -> Found PDF: {os.path.basename(pdf_path)}")
            
            safe_title = "".join(c for c in title_clue if c.isalnum() or c in (' ', '_')).replace(' ', '_').strip()
            raw_path = RAW_DIR / f"{safe_title}.txt"
            wiki_path = WIKI_DIR / "summaries" / f"summary_{safe_title}.md"
            
            if wiki_path.exists():
                print(f"  -> Summary already exists. Skipping.")
                continue
                
            print("  -> Extracting text...")
            raw_text = extract_pdf.extract_text(pdf_path)
            raw_path.write_text(raw_text, encoding="utf-8")
            
            print("  -> Generating AI Summary...")
            summary = summarize_text.generate_wiki_summary(raw_text, title_clue, reading_text, metadata)
            
            if summary:
                wiki_path.write_text(summary, encoding="utf-8")
                summarize_text.update_wiki_log(f"Batch ingested and summarized: {title_clue}")
                summarize_text.update_wiki_index("Paper Summaries", f"[{title_clue}](summaries/{wiki_path.name}) - Module: {current_module}")
                print("  -> Success!")
            else:
                print("  -> Failed to generate summary.")
                summarize_text.update_failed_ingestions(reading_text, "Gemini failed to generate a summary.")

if __name__ == "__main__":
    parse_schedule_and_ingest()
