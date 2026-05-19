# Canvas Sync CLI Tool

Command-line interface for synchronizing Canvas course pages with local markdown files.

## Setup

### 1. Install Dependencies

```bash
mamba install -r requirements.txt
```

Required packages:
- `requests` - HTTP library for Canvas API
- `markdown` - Convert markdown to HTML
- `html2text` - Convert HTML to markdown
- `frontmatter` - Handle YAML frontmatter in markdown

### 2. Add Canvas API Token

Create a `.env` file in the parent directory (one level up from `code/`):

```
CANVAS_TOKEN=your_token_here
```

To get your Canvas API token:
1. Log in to Canvas
2. Click Account → Settings
3. Under "Approved Integrations", click "New Access Token"
4. Copy the token and paste into `.env`

## Usage

```bash
# Download all Canvas pages to local markdown files
python canvas_sync.py down

# Upload all markdown files to Canvas
python canvas_sync.py up

# Specify a different course ID
python canvas_sync.py down --course 12345

# Verbose output with progress details
python canvas_sync.py up --verbose

# Get help
python canvas_sync.py --help
```

## Commands

### `down` - Download Canvas Pages

Downloads all pages from your Canvas course and saves them as markdown files with YAML frontmatter.

```bash
python canvas_sync.py down [--course COURSE_ID] [--pages-dir DIR] [--verbose]
```

**Output**: Markdown files saved to `canvas_pages/` (or custom `--pages-dir`)

**Frontmatter**: Each file includes:
```yaml
---
published: true  # or false (matches Canvas page publication status)
title: Original Page Title
---
```

### `up` - Upload Markdown to Canvas

Uploads all markdown files from the local directory to Canvas pages.

```bash
python canvas_sync.py up [--course COURSE_ID] [--pages-dir DIR] [--verbose]
```

**Input**: Markdown files from `canvas_pages/` (or custom `--pages-dir`)

**Frontmatter**: Respects `published` status:
- `published: true` → publishes page immediately
- `published: false` → saves as draft (default)

## Default Course ID

Default course ID is `14011875` (ECO 331 Spring 2026). Override with `--course`:

```bash
python canvas_sync.py up --course 11204793
```

## Examples

### Sync all pages from Canvas
```bash
python canvas_sync.py down --verbose
```

### Make changes locally, then upload
```bash
# 1. Download pages
python canvas_sync.py down

# 2. Edit markdown files in canvas_pages/

# 3. Upload changes back to Canvas
python canvas_sync.py up --verbose
```

### Work with a different course
```bash
# Download from course 12345
python canvas_sync.py down --course 12345

# ... edit files ...

# Upload back to course 12345
python canvas_sync.py up --course 12345
```

## YAML Frontmatter Guide

Each markdown file can include optional YAML frontmatter to control Canvas page settings:

```markdown
---
published: true
title: Custom Page Title
---

# Page content here

Your content...
```

**Supported fields:**
- `published` (boolean): `true` to publish, `false` to save as draft
- `title` (string): Page title (optional, defaults to filename if not specified)

If no frontmatter exists, files default to `published: false` (draft mode).

## Workflow Tips

### 1. Version Control Your Pages

Keep your `canvas_pages/` directory in git to track changes:

```bash
git add canvas_pages/
git commit -m "Update Canvas pages"
git push
```

### 2. Backup Before Upload

Always download before uploading to avoid overwriting:

```bash
python canvas_sync.py down  # Save current state
# ... make edits ...
python canvas_sync.py up    # Upload changes
```

### 3. Edit Multiple Pages

Download all pages, edit them locally in your text editor or Obsidian, then upload them all at once:

```bash
python canvas_sync.py down
# Edit canvas_pages/*.md files
python canvas_sync.py up
```

## Troubleshooting

### Error: "CANVAS_TOKEN not found"

Make sure:
1. `.env` file exists in the parent directory: `../.env`
2. File contains: `CANVAS_TOKEN=your_actual_token`
3. Token is valid (not expired)

Check the path:
```bash
# From code/ directory:
python canvas_sync.py down --verbose
```

### Error: "No pages found"

Check:
1. Course ID is correct (use `--course` flag to override)
2. You have access to the course
3. Course has at least one published page

### Module import errors

Install dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install requests markdown html2text frontmatter
```

## Related Files

- `canvastask.py` - Canvas API module (used by this tool)
- `canvas_task.ipynb` - Jupyter notebook with Canvas utilities
- `canvas_pages/` - Directory for synced markdown files

## More Information

For more Canvas API details, see the inline documentation in `canvastask.py`.
