import re
import os
import shutil
from pathlib import Path

md_file = Path(r'c:\Users\jonat\My Drive\Hunter\eco331\slides\sl_9_IR.md')
dest_dir = Path(r'c:\Users\jonat\My Drive\Hunter\eco331\slides\attachments')
source_dir = Path(r'C:\Users\jonat\My Drive\Hunter\eco330\slides\attachments')

dest_dir.mkdir(parents=True, exist_ok=True)

content = md_file.read_text(encoding='utf-8')
# Find all occurrences of image paths like attachments/xyz.png
images = re.findall(r'attachments/([^)\"\'\s]+\.(?:png|jpg|jpeg|gif))', content, re.IGNORECASE)

print(f'Found {len(images)} image references in {md_file.name}.')
missing = []
copied = []
for img in set(images):
    dest_path = dest_dir / img
    if not dest_path.exists():
        src_path = source_dir / img
        if src_path.exists():
            shutil.copy2(src_path, dest_path)
            copied.append(img)
        else:
            missing.append(img)

print(f'Checked {len(set(images))} unique images.')
print(f'Copied {len(copied)} files: {copied}')
print(f'Still missing {len(missing)} files: {missing}')
