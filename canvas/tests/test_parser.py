import re
from pathlib import Path

def parse_submissions(filepath):
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    blocks = re.split(r'\n---+\n', text)
    submissions = []
    for block in blocks:
        block = block.strip()
        name_match = re.match(r'^## (.+)', block)
        if not name_match:
            continue
        name = name_match.group(1).strip()
        content_lines = block.split('\n', 1)
        content = content_lines[1].strip() if len(content_lines) > 1 else ''
        if content and len(content) > 50:
            submissions.append({'name': name, 'content': content})
    return submissions

subs = parse_submissions(r'c:\Users\jonat\My Drive\Hunter\eco331\canvas\canvas_submits\submissions_61516335_20260313_111549.md')
print(f'Found {len(subs)} submissions')
for s in subs:
    print(f'  - {s["name"]}')
