# CLAUDE.md - ECO 331: Economic History

## Critical Rules

### 1. NEVER DELETE DATA
Under no circumstances should you delete any files or data in this project. If you need to remove something, move it to a "Legacy" folder instead.

Under no circumstances should you delete any program files. This includes '.py', '.ipynb', '.md', '.tex', or any other code or document files. If you need to remove something, move it to a "Legacy" folder instead.

## Project Overview
Course materials directory for **ECO 331: Economic History** at Hunter College, taught by Professor Jonathan Conning. Explores the historical origins of economic growth from the Neolithic Revolution through the Industrial Revolution and modern development.

## Project Structure

```
eco331/
├── .obsidian/         # Obsidian vault configuration (vault root at project level)
├── syllabus/          # Course syllabi and reading schedules
├── slides/            # Marp presentation slides (sl_*.md naming convention)
│   ├── attachments/   # Images and media files for slides and notes
│   └── pdf/           # Generated PDF versions of slides
├── notes/             # Obsidian notes: class plans, topic notes, and lecture materials
│   ├── topics/        # Topic-specific notes (Notes_*.md)
│   ├── summaries/     # Reading summaries
│   └── questions/     # Discussion questions (Q_*.md)
├── code/              # Python notebooks and scripts for economic models
├── read/              # Course readings and PDFs
│   ├── KRbook/        # Koyama & Rubin chapter materials
│   └── OGbook/        # Oded Galor book materials
├── exams/             # Exam materials
├── questions/         # Assignments
├── grades/            # Grading materials and student comments
└── templates/         # Document templates (Marp, LaTeX)
```

## Key Textbooks
- **KR**: Koyama & Rubin (2022) - *How the World Became Rich*
- **OG**: Galor (2022) - *The Journey of Humanity*

## Key Technologies

- **Obsidian**: Note-taking and knowledge management (vault root at project level, config in `.obsidian/`)
  - Attachments stored in `slides/attachments/`
- **Marp**: Markdown-based slide presentations in `slides/` directory
- **Python/Jupyter**: Data analysis and economic modeling
  - NumPy, Matplotlib for visualizations
  - Jupytext for version control of notebooks
- **Pandoc**: Document conversion (LaTeX templates available)
- **Bibliography**: BibTeX files for references (notes/Eco331.bib, notes/references.bib)

## File Naming Conventions
- `sl_N_Topic.md` - Slide decks (numbered by topic order)
- `Notes_*.md` - Topic notes
- `Q_*.md` - Question sets
- `*S26.md` - Current semester files (Spring 2026)
- `*S25.md` / `*S23.md` - Previous semester versions (Spring 2025/2023)

## Important Files

### Syllabi
- [syllabus/syllabusS26.md](syllabus/syllabusS26.md) - Spring 2026 syllabus
- [syllabus/Reading_Schedule_SP25.md](syllabus/Reading_Schedule_SP25.md) past reading schedule

### Code & Analysis
- [code/Malthusian.ipynb](code/Malthusian.ipynb) - Malthusian economic model implementation
- [code/Henrich.ipynb](code/Henrich.ipynb) - Henrich (2004) demography and cultural evolution model
- [code/regression.ipynb](code/regression.ipynb) - Statistical analysis

### Course Materials
- [notes/Class plans - Neolithic, States, Coercion.md](notes/Class%20plans%20-%20Neolithic,%20States,%20Coercion.md) - Class planning notes
- [notes/Midterm_questions.md](notes/Midterm_questions.md) - Exam question bank

## Course Topics (Slide Order)

1. **Introduction** (sl_1_Intro) - Overview and first steps
2. **Early States** (sl_2_EarlyStates) - Neolithic Revolution, bondage
3. **Geography** (sl_3_Geography) - Environmental determinism debates
4. **Malthusian Economics** (sl_4_Malthus) - Population and resource constraints
5. **Institutions** (sl_5_Institutions) - Political economy and property rights
6. **Culture** (sl_6_Culture) - Cultural evolution and economic development
7. **Transitions** (sl_7_Transitions) - Escape from Malthusian trap
8. **Industrial Revolution** (sl_9_IR) - Technological change
9. **Atlantic Trade & Slavery** (sl_10_Atlantic, sl_10_slavery) - Economic history of coerced labor

## Working with This Project

### Notes
- Notes are managed in Obsidian with interlinking and tags
- Main notes directory contains markdown files for class planning, content drafts, and bibliographic information

### Code
- Jupyter notebooks use Jupytext for syncing with Python scripts
- Run notebooks to generate economic models and visualizations
- Models include demographic transitions, skill transmission, and Malthusian dynamics

### Slides
- Slides are created using Marp (Markdown Presentation Ecosystem)
- Located in `slides/` directory at project root
- Generated PDFs stored in `slides/pdf/`
- Images for slides stored in `slides/attachments/`

### Readings
- Primary course readings in `read/` directory
- Organized by topic/book (KRbook, OGbook, Arack_Passell, etc.)

## Templates
- LaTeX template: [notes/latex.template](notes/latex.template)
- Markdown template: [notes/md.template](notes/md.template)

## Bibliography Management
- Main bibliography: [notes/Eco331.bib](notes/Eco331.bib)
- References: [notes/references.bib](notes/references.bib)

## Notes for AI Assistants

### When helping with this project:
1. **Respect academic integrity** - Don't generate exam answers or complete student assignments
2. **Maintain formatting** - Preserve Obsidian wikilinks `[[]]` and Marp slide delimiters `---`
3. **Code style** - Follow NumPy/Matplotlib conventions for analysis notebooks
4. **Citations** - Use BibTeX format when adding references
5. **File organization** - Keep materials in appropriate subdirectories
6. **Pandoc compatibility** - Ensure markdown works with pandoc conversion to PDF

### Worklog Management (CRITICAL)

- **ALWAYS update WORKLOG.md after every file change** (Edit, Write, NotebookEdit operations)
- Use format: `- [HH:MM] filename: Brief description of change`
- This provides a human-readable log of all changes made during the session
- The worklog syncs via Google Drive across all computers
- Example: `- [14:42] code/Henrich.ipynb: Added error handling for demographic model parameters`

### Common Tasks:
- Creating/updating lecture slides in Marp format
- Developing economic models in Jupyter notebooks
- Organizing reading materials and summaries
- Generating questions for exams (not answers)
- Bibliography management
- Converting between formats (MD → PDF via Pandoc)

### Course Context:
This is a **teaching** repository, not student work. Materials should support instruction and learning but maintain academic standards. The course examines long-run economic history through theoretical models, empirical evidence, and historical case studies.

## Build Commands

```bash
# Convert syllabus to PDF
pandoc syllabus/syllabusS26.md -o syllabus/syllabusS26.pdf

# Build Marp slides to PDF
marp slides/sl_1_Intro.md -o slides/pdf/sl_1_Intro.pdf

# Sync Jupytext notebook
jupytext --sync code/Henrich.ipynb
```

## Current Semester
**Spring 2026 (S26)** - See `syllabus/syllabusS26.md`
**Previous**: Spring 2025 (S25) - `syllabus/syllabusS25.md` and `syllabus/Reading_Schedule_SP25.md`
