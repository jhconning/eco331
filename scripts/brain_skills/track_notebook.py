import sys
import json
from pathlib import Path
import summarize_text

WIKI_DIR = Path(__file__).parent.parent.parent / "wiki"

def extract_notebook_text(ipynb_path):
    """Extracts markdown and code cell contents from a Jupyter Notebook."""
    try:
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        content = ""
        for cell in data.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                content += "".join(cell.get('source', [])) + "\n\n"
            elif cell.get('cell_type') == 'code':
                content += "```python\n" + "".join(cell.get('source', [])) + "\n```\n\n"
        return content
    except Exception as e:
        print(f"Error reading notebook: {e}")
        return None

def track_notebook(ipynb_path):
    path = Path(ipynb_path)
    if not path.exists():
        print(f"File not found: {ipynb_path}")
        return
        
    print(f"Analyzing Notebook: {path.name}...")
    content = extract_notebook_text(path)
    if not content:
        return
        
    WIKI_DIR.mkdir(exist_ok=True)
    wiki_path = WIKI_DIR / f"notebook_{path.stem}.md"
    
    prompt = f"""You are an expert economic historian and academic assistant managing a Course Brain Wiki for ECO 331.
I am providing you with the extracted markdown and code from a Jupyter Notebook used in the class.

Notebook File: {path.name}

Your task is to generate a summary page for this notebook.
Formatting Rules:
1. Start with the YAML frontmatter. Include the following fields:
   term: S26
   notebook_file: {path.name}
2. The H1 should be the Notebook Title (infer from content) or the filename.
3. Include a link back to the notebook file (e.g. `[Open Notebook](../{path.name})`).
4. Include a "Purpose" section explaining what this notebook calculates or demonstrates.
5. Include a "Connection to Lectures" section explaining how this computational exercise fits into the broader ECO 331 themes (like Malthusian epoch, geography, etc.).
6. Do NOT use markdown code blocks (```markdown) to wrap your entire response. Just output the raw markdown text starting with the YAML ---.

Notebook Content:
---------------------
{content[:100000]} # Truncate if extremely large
"""
    
    import os
    from google import genai
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        return

    client = genai.Client(api_key=api_key)
    
    print("Generating summary...")
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-preview',
            contents=prompt
        )
        import re
        text = response.text.strip()
        text = re.sub(r'^```markdown\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
        
        wiki_path.write_text(text.strip(), encoding="utf-8")
        summarize_text.update_wiki_log(f"Tracked and summarized notebook: {path.name}")
        summarize_text.update_wiki_index("Notebooks", f"[{path.name}]({wiki_path.name})")
        print(f"Success! Notebook summary saved to {wiki_path}")
    except Exception as e:
        print(f"Error generating summary: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python track_notebook.py <path_to_ipynb>")
        sys.exit(1)
        
    track_notebook(sys.argv[1])
