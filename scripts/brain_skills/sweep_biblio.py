import os
import re
from pathlib import Path

SCHEDULE_PATH = Path(__file__).parent.parent.parent / "canvas" / "canvas_pages" / "course_outline_and_reading_schedule.md"
WIKI_DIR = Path(__file__).parent.parent.parent / "wiki"

def sweep_biblio():
    if not SCHEDULE_PATH.exists():
        print("Schedule not found.")
        return
        
    lines = SCHEDULE_PATH.read_text(encoding="utf-8").splitlines()
    
    for line in lines:
        line = line.strip()
        if line.startswith('* ') and len(line) > 10:
            reading_text = line[2:].strip()
            
            # Figure out safe title to locate the file
            if reading_text.startswith("KR ") or " KR " in reading_text:
                match = re.search(r"KR\s*(\d+)", reading_text)
                if not match: continue
                safe_title = f"KR_Chapter_{match.group(1)}"
                
            elif reading_text.startswith("OG ") or " OG " in reading_text or reading_text.startswith("OG,"):
                match = re.search(r"OG\s*(\d+)", reading_text)
                if not match: continue
                safe_title = f"OG_Chapter_{match.group(1)}"
                
            else:
                title_match = re.search(r'"([^"]+)"', reading_text)
                title_clue = title_match.group(1) if title_match else reading_text[:30]
                safe_title = "".join(c for c in title_clue if c.isalnum() or c in (' ', '_')).replace(' ', '_').strip()
                
            # Possible file names
            wiki_path = WIKI_DIR / "summaries" / f"summary_{safe_title}.md"
            wiki_manual_path = WIKI_DIR / "summaries" / f"summary_{safe_title}_manual.md"
            
            target_path = None
            if wiki_path.exists():
                target_path = wiki_path
            elif wiki_manual_path.exists():
                target_path = wiki_manual_path
                
            if target_path:
                content = target_path.read_text(encoding="utf-8")
                
                # Check if it already has Source
                if "> **Source:**" in content:
                    continue
                    
                # Insert right after the first # H1
                parts = content.split('\n')
                new_parts = []
                inserted = False
                for p in parts:
                    new_parts.append(p)
                    if not inserted and p.startswith("# "):
                        new_parts.append(f"\n> **Source:** {reading_text}\n")
                        inserted = True
                        
                if inserted:
                    target_path.write_text('\n'.join(new_parts), encoding="utf-8")
                    print(f"Updated: {target_path.name}")

if __name__ == "__main__":
    print("Sweeping existing summaries to add bibliographic data...")
    sweep_biblio()
    print("Sweep complete.")
