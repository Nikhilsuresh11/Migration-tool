# Document Migration Readiness Tool

A full-stack tool that answers one question for every document you upload:

> **"Is this document ready to migrate to Document360? If not, what needs to change?"**

Upload a `.docx` or `.pdf` file. Get back a readiness grade, a score out of 100, an effort estimate in person-days, a list of blockers that must be fixed, and AI-generated suggestions that reference your actual document — not generic advice.

---

## How It Works

The tool runs three things in sequence when you upload a file:

**1. Parses the document** — extracts every heading, paragraph, table, image, and link from Word and PDF files. 

**2. Extracts metrics** — computes everything a migration specialist would manually audit: word count, page count, heading structure, broken links, image formats and size, table complexity, readability score, duplicate sections.

**3. Runs AI analysis** — sends the extracted text and metrics to LLaMA 3.3 70B (via Groq) which evaluates content clarity, tone consistency, structural quality, and produces document-specific suggestions. The prompt explicitly instructs the model to cite actual section titles and acronyms — not generic advice. Also fallback as google/gemma-4-26b-a4b (via openrouter)

The React frontend visualises all of this in a dashboard styled after Document360's own UI.

---
### Design Considerations & Real-World Approach

This solution is built considering real-world document migration workflows, It explicitly handles complex scenarios such as table-heavy financial reports, multi-column PDFs, embedded images and diagrams, mixed-language content, and inconsistent formatting patterns. The system adopts a hybrid approach combining deterministic metric extraction for reliability with AI-driven analysis for contextual understanding of readability, structure, and migration readiness. AI outputs are tightly controlled through prompt design to ensure document-specific insights (avoiding generic suggestions), with a fallback model strategy to maintain robustness under API limits or failures. The architecture enforces strict separation between parsing, metrics, and analysis layers, enabling modularity, testability, and scalability.

Complex Document Handling — Supports tabular data, multi-column layouts, embedded media, and noisy formatting
Hybrid Analysis Approach — Deterministic metrics + AI-driven contextual evaluation
Controlled AI Usage — Prompts enforce section-specific, non-generic insights
Resilient System Design — Multi-model fallback ensures reliability under failures
Migration-Focused Metrics — Identifies real blockers like broken links, complex tables, and content debt
Modular Architecture — Loosely coupled components for maintainability and scalability
--- 

## Project Structure

```
Migration-tool/
├── backend/
│   ├── app.py                      # Flask entry point
│   ├── config.py                   # API keys, thresholds, limits
│   ├── requirements.txt
│   ├── .env                        # Your Groq API key, Openrouter API key goes here
│   ├── parsers/
│   │   ├── docx_parser.py          # Extracts text, headings, tables, images from .docx
│   │   └── pdf_parser.py           # Same for .pdf
│   ├── metrics/
│   │   └── extractor.py            # Computes all quantitative metrics
│   ├── analysis/
│   │   └── ai_analyzer.py          # Builds the prompt, calls Groq, parses response
│   ├── services/
│   │   ├── metrics_service.py      # Service layer wrapping extractor.py
│   │   └── analysis_service.py     # Service layer wrapping ai_analyzer.py
│   ├── routes/
│   │   ├── parse_routes.py         # POST /api/parse
│   │   ├── metrics_routes.py       # POST /api/metrics
│   │   ├── analysis_routes.py      # POST /api/analyze
│   │   └── report_routes.py        # POST /api/report  ← cummulative endpoint used for UI with skimmed output from all other three routes
│   └── utils/
│       └── helpers.py              # File type detection
│
└── frontend/
    ├── src/
    │   ├── App.jsx                 # Root — manages upload/results state
    │   ├── components/
    │   │   ├── UploadScreen.jsx    # Drag-and-drop zone with loading steps
    │   │   ├── Dashboard.jsx       # Results layout — banner, metrics, tabs
    │   │   ├── tabs/
    │   │   │   ├── Overview.jsx    # Score ring, effort bars, blockers, AI analysis
    │   │   │   ├── ContentDebt.jsx # Acronyms, outdated refs, placeholders
    │   │   │   └── RawJSON.jsx     # Syntax-highlighted full API response
    │   │   └── ActionBar.jsx       # Export JSON button
    │   └── main.jsx
    ├── package.json
    └── vite.config.js              # Proxies /api/* to Flask on port 5000
```

The key design decision: `parsers/` only extracts raw content. `metrics/` only computes numbers. `analysis/` only handles AI. Routes wire them together. This makes each piece independently testable.

---

## Setup

### What you need

- Python 3.9+ (backend)
- Node.js 18+ (frontend)
- A Groq API key - https://console.groq.com
- A Openrouter API key - https://openrouter.ai/workspace (fallback)
---

### Backend

```bash
# 1. Enter the backend folder
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Groq API key
#    Open .env and set:
#    GROQ_API_KEY=your_groq_api_key_here
#    OPENROUTER_API_KEY=your_open_router_key_here

# 5. Start the Flask server
python app.py
```

Backend runs at `http://127.0.0.1:5000`



### Testing documents used (input)

https://drive.google.com/drive/folders/10WGgattvIv08c_a0UN0sojcMlZk3oe0x?usp=sharing

Evaluated against real-world document scenarios, including financial reports, large tabular datasets, academic research papers (with formulas), technical documentation, user manuals, enterprise process documents, multi-column layouts, documents containing embedded images and diagrams, mixed-language content ensuring robustness across complex and diverse content types.

---

## API Endpoints

### Main — `POST /api/report`

The single endpoint the frontend calls. Runs parsing, metrics, and AI analysis in one request and returns everything merged.

```bash
curl -X POST -F "file=@your-document.pdf" http://127.0.0.1:5000/api/report
```

**Sample Output:**
```json
{
  "success": true,
  "report_id": "e2c0da7af1db",
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
  },
  "metrics": { "...full metrics dict..." },
  "analysis": { "...full AI analysis dict..." }
}
```

### Supporting endpoints

| Endpoint | What it does |
|---|---|
| `POST /api/parse` | Extract raw structure — headings, paragraphs, tables, images |
| `POST /api/metrics` | Metrics extraction only, no AI call, fast |
| `POST /api/analyze` | AI analysis only |
| `GET /api/health` | Check server and Groq API status |

---

## Input and Output Examples

### 1. Extract Metrics (`POST /api/metrics`)

**CURL Command:**
```bash
curl -X POST http://127.0.0.1:5000/api/metrics \
  -F "file=@document.pdf"
```

**Sample Output:**
```json
{
  "success": true,
  "filename": "document.pdf",
  "file_type": "pdf",
  "metrics": {
    "word_count": 2500,
    "character_count": 15000,
    "paragraph_count": 45,
    "heading_count": 8,
    "table_count": 5,
    "images_count": 12,
    "code_block_count": 15,
    "link_count": 22,
    "readability_score": 65,
    "document360_readiness": {
      "score": 78,
      "grade": "B",
      "auto_migratable": true,
      "blockers": [
        "Contains 3 embedded images",
        "Custom formatting detected"
      ],
      "warnings": [
        "Table with merged cells",
        "Unsupported field codes"
      ]
    }
  },
  "extraction_warnings": []
}
```

---

### 2. Parse Document (`POST /api/parse`)

**CURL Command:**
```bash
curl -X POST http://127.0.0.1:5000/api/parse \
  -F "file=@document.pdf"
```

**Sample Output:**
```json
{
  "success": true,
  "filename": "document.pdf",
  "file_type": "pdf",
  "data": {
    "metadata": {
      "title": "Migration Document",
      "author": "John Doe",
      "creation_date": "2025-01-15"
    },
    "headings": [
      "Overview",
      "Architecture",
      "Implementation"
    ],
    "paragraphs": [
      "This is the first paragraph...",
      "This is the second paragraph..."
    ],
    "tables": [
      {
        "headers": ["Column 1", "Column 2"],
        "rows": [
          ["Data 1", "Data 2"]
        ]
      }
    ],
    "images": [
      {
        "filename": "image1.png",
        "size": 25600
      }
    ]
  }
}
```

---

### 3. AI Analysis (`POST /api/analyze`)

**CURL Command:**
```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -F "file=@document.pdf"
```

**Sample Output:**
```json
{
  "success": true,
  "filename": "document.pdf",
  "file_type": "pdf",
  "metrics": {
    "word_count": 3000,
    "table_count": 4,
    "images_count": 8
  },
  "analysis": {
    "migration_readiness": {
      "status": "READY",
      "confidence": 0.85
    },
    "readability_level": "Intermediate",
    "migration_effort_breakdown": {
      "overall_effort": "2-3 weeks",
      "estimated_person_days": 10
    },
    "suggestions": [
      "Consider breaking large tables into smaller sections",
      "Update outdated code examples",
      "Add more visual diagrams for clarity"
    ],
    "content_quality": {
      "completeness": 0.92,
      "clarity": 0.88,
      "accuracy": 0.95
    }
  },
  "extraction_warnings": []
}
```

---

### 4. Full Report (`POST /api/report`)

**CURL Command:**
```bash
curl -X POST http://127.0.0.1:5000/api/report \
  -F "file=@document.pdf"
```

**Sample Output:**
```json
{
  "success": true,
  "report_id": "a3f5b2c8d1e9",
  "filename": "document.pdf",
  "file_type": "pdf",
  "summary": {
    "filename": "document.pdf",
    "file_type": "pdf",
    "readiness_grade": "A",
    "readiness_score": 92,
    "auto_migratable": true,
    "overall_effort": "1-2 weeks",
    "person_days": 5,
    "status_label": "Clean",
    "blocker_count": 0,
    "warning_count": 2,
    "top_blockers": [],
    "top_warnings": [
      "Unsupported field codes",
      "Custom page headers"
    ]
  },
  "metrics": {
    "word_count": 2500,
    "table_count": 3,
    "images_count": 5,
    "document360_readiness": {
      "score": 92,
      "grade": "A",
      "auto_migratable": true
    }
  },
  "analysis": {
    "migration_readiness": {
      "status": "READY",
      "confidence": 0.95
    },
    "migration_effort_breakdown": {
      "overall_effort": "1-2 weeks",
      "estimated_person_days": 5
    }
  },
  "extraction_warnings": []
}
```


---

### 5. Health Check (`GET /api/health`)

**CURL Command:**
```bash
curl -X GET http://127.0.0.1:5000/api/health
```

**Sample Output:**
```json
{
  "status": "healthy",
  "message": "Welcome to migration stats"
}
```

---

### Frontend

```bash
# In a separate terminal, enter the frontend folder
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend runs at `http://localhost:3001`

The Vite dev server proxies all `/api/*` requests to `http://127.0.0.1:5000`, so no CORS issues during development. Both servers must be running at the same time.

---

## Using the Tool

**Upload screen** — drag and drop a `.pdf` or `.docx` file, or click to browse. Once a file is selected, click "Analyze document". The UI shows live step progress:

```
Parsing document...  →  Extracting metrics...  →  Running AI analysis...
```

<img width="1900" height="858" alt="image" src="https://github.com/user-attachments/assets/9ce2974e-6efc-4f80-bbc0-070bbe1554c5" />

<img width="1892" height="856" alt="image" src="https://github.com/user-attachments/assets/57d61fc5-63ab-4855-8b44-4405c8e29c7b" />

<img width="1889" height="853" alt="image" src="https://github.com/user-attachments/assets/eb6f9c5e-bd95-4d5b-bee4-c7440d832551" />


**Results dashboard** — the readiness banner at the top answers the core question immediately. The colour tells you the verdict at a glance: green for ready, amber for minor fixes needed, red for major rework. Everything below provides the supporting detail.

The dashboard has three tabs:

- **Overview** — readiness score (ring chart), migration effort by content type (bar chart), blockers and warnings, AI content analysis key-values, and visual content assessment
- **Content Debt** — table of undefined acronyms with suggested actions, outdated references, unresolved placeholders
- **Raw JSON** — the full API response with syntax highlighting and a one-click copy button

<img width="1606" height="790" alt="image" src="https://github.com/user-attachments/assets/e25d5c1c-7c19-454e-a78b-5274c5f6d0f5" />

<img width="1593" height="872" alt="image" src="https://github.com/user-attachments/assets/329ea1ee-6dbd-4930-87bb-ffc8b796ee19" />

<img width="1579" height="406" alt="image" src="https://github.com/user-attachments/assets/449b8358-ccdc-4890-beff-6c86d01db980" />

<img width="1575" height="671" alt="image" src="https://github.com/user-attachments/assets/555fc980-835f-4988-9004-9ef19dba8b0f" />

The action bar at the bottom lets you export the complete report as a JSON file or start a new analysis.

---

## Metrics Extracted

The five metrics the task requires, plus bonus fields relevant to Document360 migration:

| Metric | Required / Bonus | Why it matters for migration |
|---|---|---|
| Word count | ✅ Required | Scoping — larger docs need more effort |
| Total pages | ✅ Required | Direct input to effort estimation |
| Paragraph count | ✅ Required | High counts with low word counts = fragmented content |
| Heading count + distribution | ✅ Required | Reveals how the doc maps to D360 articles |
| Average words per paragraph | ✅ Required | Values >80 mean content needs splitting before import |
| Broken link count | ⭐ Bonus | Broken links become 404s in D360 — must fix before migration |
| Image count + format + size | ⭐ Bonus | Images need CDN hosting; large counts drive up effort |
| Table count + complexity | ⭐ Bonus | Complex tables (merged cells, >6 cols) don't render in D360's editor |
| Duplicate sections | ⭐ Bonus | Duplicated content fragments the knowledge base |
| Undefined acronyms | ⭐ Bonus | Readers in the new platform won't have the original context |
| Content age / staleness | ⭐ Bonus | Stale docs should be archived, not migrated |
| Language detection | ⭐ Bonus | Flags multilingual docs needing localisation handling |

---

## AI Analysis Output

The model receives the document text and extracted metrics as context, and returns:

- **Readability level** — Easy / Medium / Complex with explanation
- **Content clarity** — score out of 10 with assessment
- **Structural quality** — score out of 10, well-organized vs. fragmented
- **Tone analysis** — formal/conversational, consistency
- **Content classification** — document type, domain, audience
- **Content debt** — undefined acronyms, outdated references, unresolved placeholders
- **Migration readiness** — status label with specific details
- **Effort breakdown** — per content type with one-line reasoning per category
- **Suggestions** — each one cites a specific section title or acronym from the document

---



---



## Tools & Libraries

### Backend

| Library | Purpose |
|---|---|
| Flask | REST API framework |
| Flask-CORS | Allows the frontend to call the API from a different port |
| python-docx | Parses `.docx` files |
| PyMuPDF (fitz) | Parses `.pdf` files — text, images, tables, metadata |
| Groq SDK | LLaMA 3.3 70B for AI analysis |
| python-dotenv | Loads the Groq API key from `.env` |
| langdetect | Detects document language |
| Pygments | Detects programming languages in code blocks |
| Werkzeug | Secure file upload handling |

### Frontend

| Library | Purpose |
|---|---|
| React 18 | UI framework |
| Vite | Dev server with `/api` proxy to Flask on port 5000 |
| Tailwind CSS | Styling — Document360-inspired design system |
| Fetch API | HTTP calls to the backend (no extra dependencies) |

---

## Evaluation Criteria Coverage

| Criterion | How this submission addresses it |
|---|---|
| Accuracy of document parsing | Separate parsers for DOCX and PDF; headings extracted by paragraph style (DOCX) and font-size heuristics (PDF); tables detected via PyMuPDF's `find_tables()` |
| Relevance of metrics for migration | All 5 required metrics present + 8 bonus metrics directly relevant to Document360 migration (broken links, table complexity, image formats, content age, duplication) |
| Quality of AI-driven insights | Prompt instructs the model to cite specific section titles and acronyms found in the document; generic advice is explicitly prohibited in the system prompt |
| Practical usefulness | Single `/api/report` endpoint returns a grade, score, effort estimate, and prioritised blocker list — the exact output a migration lead needs to scope a project; React dashboard surfaces this without requiring the user to read raw JSON |
| Code quality | Parsers, metrics, analysis, services, and routes are fully separated; each module is independently importable and testable |
| Real-world scenario handling | Tested on a 132-page PDF with 639 images and 16 broken links; empty documents and corrupted files handled with graceful fallbacks throughout |
