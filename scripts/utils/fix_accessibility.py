import re
import os
import glob
import argparse

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add missing metadata dynamically
    # Extract title from frontmatter
    title_match = re.search(r'^title:\s*(.+)$', content, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.splitext(os.path.basename(file_path))[0]
    
    if 'description:' not in content:
        metadata_inject = f'title: {title}\ndescription: "ECO 331: Economic History - {title}"\nauthor: "Jonathan Conning"'
        if title_match:
            # Replace the title line with the new metadata block
            content = re.sub(rf'^title:\s*{re.escape(title)}$', metadata_inject, content, flags=re.MULTILINE)
        else:
            # If no title exists, we might need to inject it right after the first ---
            content = re.sub(r'^---$', f'---\n{metadata_inject}', content, count=1, flags=re.MULTILINE)

    # 2. Fix headings (h1 -> h6) to prevent skipping
    # Specific known bad heading patterns that frequently occur across decks
    content = content.replace("### ECO 331", "# ECO 331")
    content = content.replace("#### Galor's", "# Galor's")
    content = content.replace("### Galor's", "# Galor's")
    
    # Generic normalization: bump deeply nested headers up
    content = re.sub(r'^#### ', '## ', content, flags=re.MULTILINE)
    content = re.sub(r'^##### ', '### ', content, flags=re.MULTILINE)
    content = re.sub(r'^###### ', '#### ', content, flags=re.MULTILINE)

    # 3. Add Alt Text to Images missing it
    def replacer(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        words = alt_text.split()
        looks_like_only_directives = all(':' in w or w in ['bg', 'left', 'right', 'center', '%'] for w in words)
        
        # Also handle completely empty alt text ![]()
        if not alt_text.strip() or looks_like_only_directives:
            filename = os.path.basename(img_path)
            clean_name = os.path.splitext(filename)[0].replace('_', ' ').title()
            prefix = alt_text + " " if alt_text.strip() else ""
            new_alt = f"{prefix}Image of {clean_name}".strip()
            return f"![{new_alt}]({img_path})"
        return match.group(0) # unchanged

    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replacer, content)

    # Also fix the manual HTML images if any
    content = re.sub(
        r'<img\s+([^>]*?)src="([^"]+)"([^>]*?)>', 
        lambda m: f'<img {m.group(1)}src="{m.group(2)}" alt="Image of {os.path.basename(m.group(2))}"{m.group(3)}>' if 'alt=' not in m.group(0) else m.group(0), 
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Processed: {os.path.basename(file_path)}")

def main():
    parser = argparse.ArgumentParser(description="Fix ADA accessibility in Marp markdown files.")
    parser.add_argument('path', nargs='?', default='.', help="Directory or specific markdown file to process (defaults to current directory).")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        process_file(args.path)
    elif os.path.isdir(args.path):
        # Find all markdown files that match the slide deck pattern
        md_files = glob.glob(os.path.join(args.path, 'sl_*.md'))
        
        if not md_files:
            print(f"No slide decks found in {args.path}")
            return
            
        print(f"Found {len(md_files)} slide decks. Applying accessibility fixes...")
        for file_path in md_files:
            process_file(file_path)
    else:
        print(f"Error: Path {args.path} not found.")

if __name__ == '__main__':
    main()
