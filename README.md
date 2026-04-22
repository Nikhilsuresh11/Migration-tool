# Document Analysis & Migration Readiness API

A modular Flask backend that parses `.docx` and `.pdf` documents, extracts quantitative metrics, and provides AI-driven migration readiness analysis using Groq's LLaMA 3.3 70B Versatile model.

---

## Features

- **Document Parsing** — Extract text, headings, paragraphs, tables, images, and metadata from Word and PDF files
- **Metrics Extraction** — Word count, page count, paragraph count, heading distribution, Flesch readability score, content density, reading time
- **AI Analysis** — Readability level, content clarity, structural quality, migration readiness, and actionable suggestions
- **Full Report** — Single endpoint combining all capabilities into a comprehensive migration readiness report
- **Merged Report** — `POST /api/report` combines metrics + AI analysis with a computed summary block and report caching

---

## Project Structure

```
backend/
├── app.py                          # Flask entry point (app factory)
├── config.py                       # Centralized configuration
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (Groq API key)
├── parsers/
│   ├── docx_parser.py              # Microsoft Word document parser
│   └── pdf_parser.py               # PDF document parser (PyMuPDF)
├── metrics/
│   └── extractor.py                # Quantitative metrics computation
├── analysis/
│   └── ai_analyzer.py              # Groq AI-driven analysis
├── services/
│   ├── metrics_service.py          # Metrics extraction service layer
│   └── analysis_service.py         # AI analysis service layer
├── routes/
│   ├── parse_routes.py             # POST /api/parse
│   ├── metrics_routes.py           # POST /api/metrics
│   ├── analysis_routes.py          # POST /api/analyze, /api/analyze/full
│   └── report_routes.py            # POST /api/report, GET /api/report/<id>
└── utils/
    └── helpers.py                  # Shared utility functions
```

---

## Setup Instructions

### Prerequisites

- Python 3.9+
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
#    Edit .env and replace 'your_groq_api_key_here' with your actual key
```

### Running the Server

```bash
python app.py
```

The API will start at `http://127.0.0.1:5000`

---

## API Endpoints

### `GET /` — API Info
Returns available endpoints and API version.

### `GET /api/health` — Health Check
```json
{ "status": "healthy", "groq_configured": true }
```

### `POST /api/parse` — Parse Document
Upload a `.docx` or `.pdf` file and extract structured content.

```bash
curl -X POST -F "file=@document.pdf" http://127.0.0.1:5000/api/parse
```

**Response:**
```json
{
  "success": true,
  "filename": "document.pdf",
  "file_type": "pdf",
  "data": {
    "full_text": "...",
    "headings": [{"text": "Introduction", "level": 1}],
    "paragraphs": ["..."],
    "tables": [],
    "images_count": 2,
    "metadata": {"author": "...", "title": "..."}
  }
}
```

### `POST /api/metrics` — Extract Metrics
Upload a document and get quantitative analysis.

```bash
curl -X POST -F "file=@document.docx" http://127.0.0.1:5000/api/metrics
```

**Response:**
```json
{
  "success": true,
  "filename": "document.docx",
  "metrics": {
    "total_pages": 5,
    "word_count": 1250,
    "paragraph_count": 18,
    "heading_count": 6,
    "sentence_count": 62,
    "avg_words_per_paragraph": 69.44,
    "flesch_reading_ease": 58.3,
    "readability_level": "Medium",
    "estimated_reading_time_minutes": 6.3
  }
}
```

### `POST /api/analyze` — AI Analysis
Upload a document for AI-driven quality and migration readiness analysis.

```bash
curl -X POST -F "file=@document.pdf" http://127.0.0.1:5000/api/analyze
```

### `POST /api/analyze/full` — Full Migration Report
Complete report combining parsing, metrics, and AI analysis.

```bash
curl -X POST -F "file=@document.pdf" http://127.0.0.1:5000/api/analyze/full
```

---

### `POST /api/report` — Merged Report (New)

Generates a single merged response combining metrics extraction and AI analysis with a computed summary block. Reports are cached by file hash for subsequent retrieval.

```bash
curl -X POST -F "file=@document.pdf" http://127.0.0.1:5000/api/report
```

**Response (HTTP 200):**
```json
{
  "success": true,
  "report_id": "a1b2c3d4e5f6",
  "summary": {
    "filename": "document.pdf",
    "file_type": "pdf",
    "readiness_grade": "B",
    "readiness_score": 80,
    "auto_migratable": true,
    "overall_effort": "Medium",
    "person_days": 1.5,
    "status_label": "Needs minor fixes",
    "blocker_count": 0,
    "warning_count": 2,
    "top_blockers": [],
    "top_warnings": [
      "3 externally referenced image(s) — may break after migration",
      "Long paragraphs (avg 95 words) — consider breaking into smaller sections"
    ]
  },
  "metrics": { "...full metrics dict..." },
  "analysis": { "...full AI analysis dict or null if AI failed..." },
  "file_type": "pdf",
  "filename": "document.pdf",
  "extraction_warnings": []
}
```

**Summary fields breakdown:**

| Field | Source | Description |
|-------|--------|-------------|
| `readiness_grade` | Computed (metrics) | A/B/C/D from `document360_readiness.grade` |
| `readiness_score` | Computed (metrics) | 0–100 from `document360_readiness.score` |
| `auto_migratable` | Computed (metrics) | Boolean from `document360_readiness.auto_migratable` |
| `overall_effort` | AI-generated | "Low" / "Medium" / "High" from `migration_effort_breakdown` |
| `person_days` | Computed (server) | Formula-based estimate from metrics + AI scores |
| `status_label` | Computed (metrics) | Derived from readiness_score thresholds |
| `blocker_count` | Computed (metrics) | Count of `document360_readiness.blockers` |
| `warning_count` | Computed (metrics) | Count of `document360_readiness.warnings` |
| `top_blockers` | Computed (metrics) | First 3 blocker strings |
| `top_warnings` | Computed (metrics) | First 3 warning strings |

**Response headers:**

| Header | Example | Description |
|--------|---------|-------------|
| `X-Processing-Time` | `4.231` | Total processing time in seconds |
| `X-Readiness-Grade` | `B` | Document readiness grade |
| `X-Auto-Migratable` | `true` | Whether the document can be auto-migrated |

**Error responses:**

Unsupported file type (HTTP 400):
```json
{
  "success": false,
  "error": "unsupported_file",
  "detail": "Unsupported file type: .txt. Only .pdf and .docx are accepted."
}
```

Metrics extraction failure (HTTP 422):
```json
{
  "success": false,
  "error": "metrics_extraction_failed",
  "detail": "Failed to open PDF file: file is corrupted"
}
```

AI analysis failure (HTTP 200 with null analysis):
```json
{
  "success": true,
  "report_id": "a1b2c3d4e5f6",
  "summary": { "...computed from metrics only..." },
  "metrics": { "...full metrics..." },
  "analysis": null,
  "extraction_warnings": ["AI analysis failed: Groq API call failed: rate limit exceeded"]
}
```

### `GET /api/report/<report_id>` — Cached Report Retrieval (New)

Retrieve a previously generated report by its ID (first 12 chars of file SHA-256).

```bash
curl http://127.0.0.1:5000/api/report/a1b2c3d4e5f6
```

Returns the same JSON body as the original `POST /api/report` response, or 404 if the report has been evicted (max 20 cached reports, LRU eviction).

---

## Tools & Libraries

| Library | Purpose |
|---------|---------|
| Flask | Web framework for REST API |
| Flask-CORS | Cross-Origin Resource Sharing |
| python-docx | Microsoft Word .docx parsing |
| PyMuPDF (fitz) | PDF document parsing |
| Groq SDK | AI analysis via LLaMA 3.3 70B |
| python-dotenv | Environment variable management |
| Werkzeug | File upload security |
| langdetect | Language detection |
| Pygments | Code language detection |
