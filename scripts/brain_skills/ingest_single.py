import sys
import os
import glob
from pathlib import Path

# Try to import Zotero, but don't fail if it's missing (allows other scripts to run)
try:
    from pyzotero import zotero
except ImportError:
    pass

import extract_pdf
import summarize_text

RAW_DIR = Path(__file__).parent.parent.parent / "raw"
WIKI_DIR = Path(__file__).parent.parent.parent / "wiki"
ZOT_DIR = r"C:\MyGDrive\B\zot_pdfs"

def ingest_single(search_query):
    # This requires Zotero API config, which we assume is set in env or a local config
    user_id = os.environ.get("ZOTERO_USER_ID")
    api_key = os.environ.get("ZOTERO_API_KEY")
    
    if not user_id or not api_key:
        print("ERROR: Please set ZOTERO_USER_ID and ZOTERO_API_KEY environment variables.")
        return
        
    zot = zotero.Zotero(user_id, 'user', api_key)
    
    print(f"Searching Zotero for: {search_query}...")
    results = zot.items(q=search_query)
    
    parent_item = next((item for item in results if item['data'].get('itemType') != 'attachment'), None)
    if not parent_item:
        print("No parent item found.")
        return
        
    title = parent_item['data'].get('title', 'Unknown')
    print(f"Found item: {title}")
    
    # Try to find local PDF
    pdf_attachment = next((child for child in zot.children(parent_item['key']) 
                          if child['data'].get('contentType') == 'application/pdf'), None)
                          
    expected_filename = pdf_attachment['data'].get('filename', '') if pdf_attachment else ''
    
    local_pdf = None
    if expected_filename:
        fallback_path = os.path.join(ZOT_DIR, expected_filename)
        if os.path.exists(fallback_path):
            local_pdf = fallback_path
            
    if not local_pdf:
        # Fallback to fuzzy match
        import ingest_batch
        local_pdf = ingest_batch.find_pdf_fuzzy(title[:30])
        
    if not local_pdf:
        print("Could not find local PDF.")
        return
        
    print(f"Found local PDF: {local_pdf}")
    
    RAW_DIR.mkdir(exist_ok=True)
    WIKI_DIR.mkdir(exist_ok=True)
    
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_')).replace(' ', '_').strip()
    raw_path = RAW_DIR / f"{safe_title}.txt"
    wiki_path = WIKI_DIR / f"summary_{safe_title}.md"
    
    print("Extracting text...")
    raw_text = extract_pdf.extract_text(local_pdf)
    raw_path.write_text(raw_text, encoding="utf-8")
    
    print("Generating AI Summary...")
    metadata = {'module': 'Unassigned', 'assigned': 'false'}
    summary = summarize_text.generate_wiki_summary(raw_text, title, "Zotero Query", metadata)
    
    if summary:
        wiki_path.write_text(summary, encoding="utf-8")
        summarize_text.update_wiki_log(f"Single ingested and summarized: {title}")
        summarize_text.update_wiki_index("Paper Summaries", f"[{title}]({wiki_path.name})")
        print("Success!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_single.py <search_query>")
        sys.exit(1)
    ingest_single(sys.argv[1])
