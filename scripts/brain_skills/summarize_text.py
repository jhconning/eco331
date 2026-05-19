import os
import re
from pathlib import Path
from google import genai

# Load Gemini API Key
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / "canvas"))
try:
    import canvastask
    canvastask.load_env(str(Path(__file__).parent.parent.parent / '.env'))
except ImportError as e:
    print(f"Warning: Could not import canvastask to load env: {e}")

def generate_wiki_summary(raw_text, title, author_date, metadata_tags=None):
    """
    Passes raw extracted PDF text to Gemini to generate a structured Wiki summary.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        return None
    api_key = api_key.strip('"').strip("'")

    if not metadata_tags:
        metadata_tags = {}

    client = genai.Client(api_key=api_key)
    
    # Ensure text is not too large for the prompt window
    max_chars = 400000 
    if len(raw_text) > max_chars:
        raw_text = raw_text[:max_chars] + "\n\n[TEXT TRUNCATED FOR LENGTH]"

    prompt = f"""You are an expert economic historian and academic assistant managing a Course Brain Wiki for ECO 331.
I am providing you with the raw text extracted from an academic paper or book chapter.

Title: {title}
Author/Date: {author_date}

Your task is to generate a comprehensive markdown summary page for this text. 
This page will be saved in the course wiki.

Formatting Rules:
1. Start with the YAML frontmatter. Include the following fields:
   term: S26
   assigned: {metadata_tags.get('assigned', 'true')}
   student_presentation: {metadata_tags.get('student_presentation', 'false')}
   module: {metadata_tags.get('module', '')}
   associated_slide_deck: {metadata_tags.get('associated_slide_deck', '')}
2. The H1 should be the Title.
3. Immediately below the H1, you MUST include the full bibliographic reference as a blockquote, formatted as:
   > **Source:** {author_date}
4. Include an "Overview" section.
4. Include a "Core Arguments & Mechanisms" section.
5. Include a "Connections to Course Themes" section (specifically relating it to economic history, the Malthusian epoch, institutions, culture, geography, or the demographic transition).
6. Do NOT use markdown code blocks (```markdown) to wrap your entire response. Just output the raw markdown text starting with the YAML ---.

Raw Text:
---------------------
{raw_text}
"""
    
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-preview',
            contents=prompt
        )
        # Clean up any potential markdown code block wrapping
        text = response.text.strip()
        text = re.sub(r'^```markdown\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
        return text.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None

def generate_zero_shot_summary(chapter_info, metadata_tags=None):
    """
    Passes a chapter title to Gemini to generate a structured Wiki summary from pre-trained knowledge.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        return None
    api_key = api_key.strip('"').strip("'")

    if not metadata_tags:
        metadata_tags = {}

    client = genai.Client(api_key=api_key)
    
    prompt = f"""You are an expert economic historian and academic assistant managing a Course Brain Wiki for ECO 331.
I am asking you to generate a detailed academic summary based ENTIRELY on your pre-trained knowledge base.

Target Chapter: {chapter_info}

Your task is to generate a comprehensive markdown summary page for this chapter. 
This page will be saved in the course wiki.

Formatting Rules:
1. Start with the YAML frontmatter. Include the following fields:
   term: S26
   assigned: {metadata_tags.get('assigned', 'true')}
   student_presentation: {metadata_tags.get('student_presentation', 'false')}
   module: {metadata_tags.get('module', '')}
   associated_slide_deck: {metadata_tags.get('associated_slide_deck', '')}
2. The H1 should be the Chapter Title.
3. Immediately below the H1, you MUST include the full bibliographic reference as a blockquote, formatted as:
   > **Source:** {chapter_info}
4. Include an "Overview" section.
4. Include a "Core Arguments & Mechanisms" section.
5. Include a "Connections to Course Themes" section (specifically relating it to economic history, the Malthusian epoch, institutions, culture, geography, or the demographic transition).
6. Do NOT use markdown code blocks (```markdown) to wrap your entire response. Just output the raw markdown text starting with the YAML ---.
"""
    
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-preview',
            contents=prompt
        )
        # Clean up any potential markdown code block wrapping
        text = response.text.strip()
        text = re.sub(r'^```markdown\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
        return text.strip()
    except Exception as e:
        print(f"Error generating zero-shot summary: {e}")
        return None

def update_wiki_log(action_description):
    """Appends an entry to the wiki log."""
    log_path = Path(__file__).parent.parent.parent / "wiki" / "log.md"
    from datetime import datetime
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    if not log_path.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text("# ECO 331 Wiki Log\n\n", encoding="utf-8")
        
    with open(log_path, 'a', encoding="utf-8") as f:
        f.write(f"## [{date_str}] sys | {action_description}\n")

def update_wiki_index(section, entry_text):
    """Adds a link to the wiki index."""
    index_path = Path(__file__).parent.parent.parent / "wiki" / "index.md"
    if not index_path.exists():
        return
        
    content = index_path.read_text(encoding="utf-8")
    
    # Simple regex to insert under the correct section
    import re
    section_pattern = re.compile(rf"(## {section}\n[^\n]*\n)", re.IGNORECASE)
    
    if section_pattern.search(content):
        new_content = section_pattern.sub(rf"\1- {entry_text}\n", content)
        index_path.write_text(new_content, encoding="utf-8")
    else:
        # If section doesn't exist, append it
        with open(index_path, 'a', encoding="utf-8") as f:
            f.write(f"\n## {section}\n- {entry_text}\n")

def update_failed_ingestions(reading_text, reason):
    """Logs a reading that failed to ingest so the user can manually resolve it."""
    failed_path = Path(__file__).parent.parent.parent / "wiki" / "failed_ingestions.md"
    
    if not failed_path.exists():
        failed_path.parent.mkdir(parents=True, exist_ok=True)
        failed_path.write_text("# Failed Ingestions\n\nThe following readings could not be automatically ingested into the Course Brain. To resolve them, paste the absolute path to the local PDF next to **Manual PDF Path:** and run `python scripts/brain_skills/retry_failed.py`.\n\n", encoding="utf-8")
        
    with open(failed_path, 'a', encoding="utf-8") as f:
        f.write(f"- **Reading:** {reading_text}\n  - **Reason:** {reason}\n  - **Manual PDF Path:** \n\n")

