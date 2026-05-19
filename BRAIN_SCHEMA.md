# ECO 331 Course Brain Schema

This document outlines the architecture and standard operating procedures for the ECO 331 Course Brain, an LLM-maintained local Wiki designed to track readings, audit slides, and synthesize class progress.

## 1. Directory Architecture

The system enforces a strict boundary between immutable human-authored content and mutable AI-generated knowledge.

### Immutable Core (Human-Authored)
The AI **reads** these folders but **never modifies** them.
*   `slides/`: Markdown lecture slides.
*   `syllabus/`: Core course policies.
*   `code/` & `scripts/`: Manual scripts and Jupyter Notebooks.
*   `raw/`: Raw, unedited text extractions from Zotero PDFs.

### The Active Wiki (AI-Maintained)
The AI **owns** this layer and updates it incrementally.
*   `wiki/`: The central knowledge base containing:
    *   `index.md`: A maintained catalog of everything in the wiki.
    *   `log.md`: An append-only chronological record of AI actions.
    *   `failed_ingestions.md`: Automatically tracks readings that failed to ingest, providing a space for users to input manual paths or `IGNORE` tags.
    *   `ignored_readings.md`: Persistent list of readings to completely skip during batch ingestion.
    *   `summaries/`: LLM-generated summaries of `raw/` texts (`summary_*.md`).
    *   `notebooks/`: Explanations of `.ipynb` files and their relevance (`notebook_*.md`).
    *   `audits/`: Suggested modifications for slides based on new readings (`audit_*.md`).
*   `canvas/`: Toolkit and downloaded assessments. 
    *   `canvas_submits/summary/`: AI summaries of student submissions.

## 2. Global YAML Frontmatter

All documents within the `wiki/`, `slides/`, and `raw/` directories MUST contain standardized YAML frontmatter for cross-referencing.

```yaml
---
term: S26
module: M3_Geography  # Reference to the module mapped in course_modules.md
assigned: true        # Is this required reading?
student_presentation: false
associated_slide_deck: sl_3_Geography.md
---
```

## 3. The Orchestration Layer

**`course_modules.md`** (located in the project root):
This is the master mapping document. Instead of hard-coding the schedule into every individual slide, this file links:
*Date → Slide Deck → Assigned Readings → Canvas Assignments*.

## 4. Workflows

### A. Ingestion (Adding Knowledge)
1. **Raw Extraction**: The AI extracts text from a PDF (located in `C:\MyGDrive\B\zot_pdfs` or manually provided) and saves it to `raw/`.
2. **Summarization**: The AI reads the `raw/` text, generates a summary page in `wiki/` (with YAML tags), and links it to relevant concepts. Summaries automatically embed a `> **Source:**` bibliographic blockquote right below the H1 Title.
3. **Bookkeeping**: The AI updates `wiki/index.md` and appends an entry to `wiki/log.md`.

*Trigger Methods:*
*   **Single**: Via Zotero API query (`ingest_single.py`).
*   **Batch**: By parsing `canvas/canvas_pages/course_outline_and_reading_schedule.md` and fuzzy-matching titles to local PDFs (`ingest_batch.py`).
*   **Special Textbooks (KR/OG)**: Zero-shot generation or automatic text extraction from local teaching materials (`.pptx` or `.md`) in `read/KRbook/` when a PDF is unavailable.
*   **Manual Retries**: Processing user-provided absolute paths via `failed_ingestions.md` using `retry_failed.py`.

### B. Notebook Tracking
When a Jupyter Notebook is added or updated, the AI analyzes the `.ipynb` file and generates a summary markdown page in the `wiki/`. The page includes a link back to the notebook and explains how it fits into the lecture topics.

### C. Slide Auditing
You ask the AI to evaluate an existing slide deck against a new reading. The AI reads both, notes gaps or misconceptions, and writes an audit report to `wiki/` (e.g., `audit_acemoglu_sl_3.md`). 

**Important:** Every Audit must begin with a summary of the slide deck's content and its main broad themes before diving into the specific critiques or suggested modifications. Furthermore, every audit MUST conclude with the following two explicitly labeled sections (which may synthesize or repeat actionable items from above):
1. `### Suggested slide deletion or reorganization`
2. `### Suggested slide additions`

It updates the index and log accordingly.
