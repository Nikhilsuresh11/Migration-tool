# Document Analysis & Migration Readiness Tool

A Flask-based automation tool that answers one question for every document you upload:

> **"Is this document ready to migrate to Document360? If not, what needs to change?"**

It parses `.docx` and `.pdf` files, extracts structural metrics, and uses AI (LLaMA 3.3 70B via Groq) to produce a readiness grade, effort estimate, and specific improvement suggestions — all in a single API call.

---

## What This Tool Does

When you upload a document, the tool runs three things in sequence:

**1. Parses the document** — extracts every heading, paragraph, table, image, and link from Word and PDF files. It handles edge cases like empty documents, password-protected files, and documents with inconsistent formatting.

**2. Extracts metrics** — counts everything that matters for a migration: word count, page count, heading structure, broken links, image count and format, table complexity, readability score, and more. These are the numbers a migration specialist would manually audit before starting a project.

**3. Runs AI analysis** — sends the extracted text and metrics to an LLM that evaluates content clarity, tone consistency, structural quality, and produces specific, document-aware suggestions (not generic advice). It also flags content debt: undefined acronyms, outdated references, and unresolved placeholders.

The final output is a readiness grade (A/B/C/D), a score out of 100, an effort estimate in person-days, and a list of blockers that must be fixed before migration can begin.

---

## Project Structure

```
backend/
├── app.py                      # Flask entry point
├── config.py                   # API keys, file size limits, thresholds
├── requirements.txt
├── .env                        # Your Groq API key goes here
│
├── parsers/
│   ├── docx_parser.py          # Extracts text, headings, tables, images from .docx
│   └── pdf_parser.py           # Extracts same from .pdf using PyMuPDF
│
├── metrics/
│   └── extractor.py            # Computes all quantitative metrics
│                               # (readability, links, duplication, tables, media, etc.)
│
├── analysis/
│   └── ai_analyzer.py          # Builds the prompt, calls Groq, parses the response
│
├── services/
│   ├── metrics_service.py      # Service layer wrapping extractor.py
│   └── analysis_service.py     # Service layer wrapping ai_analyzer.py
│
├── routes/
│   ├── parse_routes.py         # POST /api/parse
│   ├── metrics_routes.py       # POST /api/metrics
│   ├── analysis_routes.py      # POST /api/analyze
│   └── report_routes.py        # POST /api/report  ←  main endpoint
│
└── utils/
    └── helpers.py              # File type detection, temp file cleanup, hashing
```

The key design decision: `parsers/` only extracts raw content. `metrics/` only computes numbers. `analysis/` only handles AI. Routes wire them together. This separation makes each piece independently testable.

---

## Setup

### What you need

- Python 3.9 or higher
- A Groq API key — free at [console.groq.com](https://console.groq.com)

### Install

```bash
# Clone and enter the backend folder
cd backend

# Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
# Open .env and replace the placeholder:
# GROQ_API_KEY=your_groq_api_key_here
```

### Run

```bash
python app.py
```

API is now running at `http://127.0.0.1:5000`

---

## API Endpoints

### Main endpoint — `POST /api/report`

This is the one endpoint that does everything. Upload a file, get back a complete migration readiness report.

```bash
curl -X POST -F "file=@your-document.pdf" http://127.0.0.1:5000/api/report
```

Returns a `summary` block (the headline verdict), a full `metrics` block (all computed numbers), and a full `analysis` block (AI-generated insights).

The summary block answers the migration question directly:

```json
{
  "summary": {
    "filename": "product-guide.pdf",
    "readiness_grade": "C",
    "readiness_score": 65,
    "status_label": "Major rework required",
    "auto_migratable": false,
    "overall_effort": "High",
    "person_days": 2.5,
    "blocker_count": 2,
    "top_blockers": [
      "16 broken links detected — must be fixed before migration",
      "2 complex tables (>6 cols or >20 rows) — need restructuring"
    ],
    "warning_count": 1,
    "top_warnings": [
      "Long paragraphs (avg 93 words) — consider splitting"
    ]
  }
}
```

Response headers also carry key values for programmatic use:

```
X-Processing-Time: 4.23
X-Readiness-Grade: C
X-Auto-Migratable: false
```

---

### Supporting endpoints

| Endpoint | What it does |
|---|---|
| `POST /api/parse` | Extract raw structure (headings, paragraphs, tables) from a document |
| `POST /api/metrics` | Run metrics extraction only — no AI call |
| `POST /api/analyze` | Run AI analysis only — pass in a document |
| `GET /api/report/<id>` | Retrieve a cached report by its ID |
| `GET /api/health` | Check if the server and Groq API are configured |

Reports are cached by file hash (SHA-256). The last 20 reports are kept in memory. The `report_id` returned by `/api/report` can be used with `GET /api/report/<id>` to retrieve the same result without re-processing.

---

## Metrics Extracted

These map directly to what a migration specialist checks before starting a project:

| Metric | Why it matters for migration |
|---|---|
| Word count + reading time | Scoping — larger docs need more effort |
| Page count | Direct input to effort estimation |
| Heading distribution (H1–H6) | Reveals whether the doc can be split into D360 articles |
| Average words per paragraph | High values (>80) mean content needs splitting before import |
| Flesch readability score | Flags content that needs rewriting for a general audience |
| Broken link count | Broken links must be fixed before migration — they become 404s |
| Image count + formats + size | Images need CDN hosting; large counts drive up effort |
| Table count + complexity | Complex tables (merged cells, >6 cols) don't render in D360's editor |
| Duplicate sections | Duplicated content fragments the knowledge base |
| Undefined acronyms | Readers in the new platform won't have original context |
| Content age / staleness | Stale docs should be archived, not migrated |
| Language detection | Flags multilingual docs that need localization handling |

Beyond the required metrics (pages, words, paragraphs, headings, avg words/para), all additional fields above are bonus insights relevant to real migration work.

---

## AI Analysis

The AI analysis uses LLaMA 3.3 70B (via Groq) with a system prompt that establishes a migration specialist persona. The model receives the document text and the extracted metrics as context, and returns structured JSON covering:

- **Readability level** — Easy / Medium / Complex with explanation
- **Content clarity** — Score out of 10 with assessment
- **Structural quality** — Score out of 10, well-organized vs. fragmented
- **Tone analysis** — Formal/conversational, consistency, passive voice ratio
- **Content classification** — Document type, domain, audience, whether it's evergreen
- **Content debt** — Undefined acronyms, outdated references, unresolved placeholders, broken cross-references
- **Migration readiness** — Status label, specific details
- **Migration effort breakdown** — Per content type (text, images, tables, links, structure) with reasoning
- **IA mapping suggestion** — Suggested Document360 category, slug, and article breakdown
- **Visual content assessment** — Image-to-text ratio, accessibility risk, alt text status
- **Suggestions** — Document-specific, referencing actual section titles and acronyms found

The prompt explicitly instructs the model to never give generic advice — every suggestion must reference something found in the actual document.

---

## Sample Input & Output

### Input
Any `.docx` or `.pdf` file. Tested with:
- A 132-page annual report (PDF, 639 images, 12,338 words) → Grade C
- A 32-page startup report (DOCX, 640 images, 7,967 words) → Grade A
- A 41-page research paper (PDF, 11 images, 12,393 words) → Grade B

### Output — Abridged

```json
{
  "success": true,
  "report_id": "e2c0da7af1db",
  "summary": {
    "filename": "Indus valley annual report 2024.pdf",
    "file_type": "pdf",
    "readiness_grade": "C",
    "readiness_score": 65,
    "status_label": "Major rework required",
    "auto_migratable": false,
    "overall_effort": "Medium",
    "person_days": 2.5,
    "blocker_count": 2,
    "top_blockers": [
      "16 broken links detected — must be fixed before migration",
      "2 complex tables (>6 cols or >20 rows) — may need restructuring"
    ],
    "warning_count": 1,
    "top_warnings": [
      "Long paragraphs (avg 93.47 words) — consider breaking into smaller sections"
    ]
  },
  "metrics": {
    "word_count": 12338,
    "total_pages": 132,
    "paragraph_count": 132,
    "heading_count": 51,
    "avg_words_per_paragraph": 93.47,
    "flesch_reading_ease": 39.75,
    "readability_level": "Complex",
    "links": {
      "broken_links": 16,
      "external_links": 34
    },
    "tables": {
      "table_count": 112,
      "complex_tables": 2,
      "tables_with_headers": 107
    },
    "media": {
      "images_count": 639,
      "total_media_size_mb": 19.3,
      "image_formats": { "jpeg": 493 }
    },
    "document360_readiness": {
      "grade": "C",
      "score": 65,
      "auto_migratable": false,
      "manual_effort_hours_estimated": 11.0
    }
  },
  "analysis": {
    "readability_level": "Complex",
    "content_clarity": { "score": 6, "assessment": "..." },
    "structural_quality": { "score": 8, "assessment": "well-organized" },
    "migration_readiness": { "status": "Major rework required" },
    "content_debt": {
      "abbreviations_without_definition": ["GFCF", "SIPs"],
      "outdated_references_detected": ["last year", "next quarter"],
      "content_debt_score": 4
    },
    "suggestions": [
      "Section 'How to read this report' averages 156 words per paragraph — split into sub-sections with sub-headings.",
      "The acronym 'GFCF' is used without prior definition — expand on first use.",
      "Section 'India's Discretionaries spend' contains a complex chart — add a brief text summary below it."
    ]
  }
}
```

---

## Tools & Libraries

| Library | Purpose |
|---|---|
| Flask | REST API framework |
| Flask-CORS | Allows the frontend to call the API |
| python-docx | Parses `.docx` files |
| PyMuPDF (fitz) | Parses `.pdf` files — text, images, tables, metadata |
| Groq SDK | LLaMA 3.3 70B for AI analysis |
| python-dotenv | Loads the Groq API key from `.env` |
| langdetect | Detects document language |
| Pygments | Detects programming languages in code blocks |
| Werkzeug | Secure file upload handling |

---

## Error Handling

The tool handles real-world document problems without crashing:

- **Empty documents** — returns metrics with zero counts, skips AI call
- **Corrupted files** — returns HTTP 422 with a readable error message
- **Wrong file type** — returns HTTP 400, only `.pdf` and `.docx` accepted
- **AI call failure** — returns HTTP 200 with `analysis: null` and a warning; metrics still returned
- **Large documents** — text is truncated to fit the model's context window; a warning is added to `extraction_warnings`
- **Missing metadata** — all metadata fields default to `null`, never crash the response

---

## Evaluation Criteria Coverage

| Criterion | How this submission addresses it |
|---|---|
| Accuracy of document parsing | Separate parsers for DOCX and PDF; headings extracted by style (DOCX) and font size heuristics (PDF); tables detected via PyMuPDF's `find_tables()` |
| Relevance of metrics for migration | All 5 required metrics present + 10 bonus metrics directly relevant to Document360 migration (broken links, table complexity, image formats, content age, duplication) |
| Quality of AI-driven insights | Prompt instructs model to cite specific section titles and acronyms; generic advice is explicitly prohibited in the system prompt |
| Practical usefulness | Single `/api/report` endpoint returns a grade, score, effort estimate, and prioritised blocker list — the exact output a migration lead needs to scope a project |
| Code quality | Parsers, metrics, analysis, and routes are fully separated; each module is independently importable and testable |
| Real-world scenario handling | Tested on a 132-page PDF with 639 images and 16 broken links; empty doc and corrupted file edge cases handled |