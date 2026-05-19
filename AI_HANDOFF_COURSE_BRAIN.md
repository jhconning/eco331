# ECO 331 "Course Brain" - AI Handoff Document

> **To the AI Agent:** The user is starting a fresh session to build a local, markdown-driven Learning Management System (the "Course Brain") for their ECO 331 Economic History class. Please read this document to load the architectural vision and immediate next steps into your working memory.

## 1. Project Vision
The goal is to transition away from static LMS platforms (like Canvas) into an active, queryable local Wiki. This system will allow the user to cross-reference lecture slides, academic readings, and student assessment data to automatically audit the curriculum, identify student misconceptions, and dynamically generate reviews.

## 2. Directory Structure & Current State
**Root Path:** `C:\MyGDrive\Hunter\eco331`

The directory currently contains subfolders for slides (e.g., `slides\sl_3_Geography.md`, `slides\sl_7b_LandAbundant.md`), some Canvas integration scripts (`canvas\`), and miscellaneous python files.

The intended architecture for the Course Brain is:
- `readings/`: For full-text markdown extractions of syllabus papers.
- `slides/`: Already exists; contains markdown versions of lectures.
- `assessments/`: A staging area for Canvas bulk-downloads (student responses).
- `synthesis/`: For AI-generated audits and misconception heatmaps.

## 3. Immediate Next Steps for the AI
When the user is ready, execute the following steps in order:

### Phase 1: Globalize the Ingestion Skill
1. Locate the local Zotero ingestion script at `C:\MyGDrive\B\wiki\scripts\ingest_from_zotero.py`.
2. Refactor it into a global Antigravity Skill located at `C:\Users\jonat\.agents\skills\zotero-ingest\`.
3. Modify it to accept a target output directory (so it can output to `eco331\readings\`) and parameterize the Zotero tagging (e.g., tag as `_eco331_reading` instead of `_ingested_wiki`).

### Phase 2: Ingest the Syllabus
1. Run the newly globalized skill to pull down the core ECO 331 readings from Zotero into the `eco331\readings\` folder as Markdown files.

### Phase 3: Slide Auditing & Linking
1. Parse the existing markdown slides in `eco331\slides\`.
2. Demonstrate a "Curriculum Audit" by querying the AI to cross-reference a specific slide deck against a newly ingested reading, suggesting bullet points to add or concepts to clarify based on the literature.

## 4. Standard Operating Procedures
- **Context:** Always operate with the assumption that `C:\MyGDrive` is the trusted primary path.
- **Logging:** After every significant architectural change or batch ingestion, you MUST update the global worklog at `C:\MyGDrive\B\notable\Main notes\gemini\master_worklog.md`.
