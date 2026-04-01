# 🧠 Meeting Intelligence Hub

> Transform raw meeting transcripts into actionable intelligence — automatically surfacing decisions, action items, and answers to questions so teams can stop re-reading and start executing.

Built for the Cymonic Technologies Campus Recruitment 2026 Technical Challenge.

---

## ❗ The Problem

Teams often spend significant time manually reviewing meeting transcripts to identify key decisions and assigned tasks. Important information can be missed, leading to miscommunication and delays in execution.

---

## 💡 The Solution

Meeting Intelligence Hub automatically processes meeting transcripts using AI to extract decisions, action items, and key insights. It also provides a chatbot interface for querying transcripts and supports exporting structured results, enabling teams to quickly act on meeting outcomes.

--

## 🚀 Features

- **Decision & Action Item Extractor** — Automatically identifies decisions made and tasks assigned from any meeting transcript
- **Multi-format Support** — Accepts both `.txt` and `.vtt` (WebVTT) transcript formats
- **Contextual Query Chatbot** — Ask natural language questions across uploaded transcripts and get cited answers
- **Export** — Download decisions and action items as CSV or PDF
- **Clean UI** — Drag-and-drop upload, structured tables, and a chat interface

---

## 🛠️ Tech Stack

## 🛠️ Tech Stack

| Category             | Technology               |
| -------------------- | ------------------------ |
| Programming Language | Python                   |
| Frontend             | Streamlit                |
| Backend              | FastAPI                  |
| LLM API              | Groq API (Llama 3.3 70B) |
| Data Processing      | Pandas                   |
| PDF Export           | ReportLab                |

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10 or higher
- A Groq API key (free at [console.groq.com](https://console.groq.com))

### Step 1 — Clone the repository

```bash
git clone https://github.com/jeromemathew2004/meeting-intelligence-hub.git
cd meeting-intelligence-hub
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and add your API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com) — no credit card required.

### Step 5 — Run the backend

```bash
uvicorn api.main:app --reload
```

API will be running at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### Step 6 — Run the frontend (new terminal)

```bash
streamlit run frontend/app.py
```

App will be running at `http://localhost:8501`

---

## 📁 Project Structure

```
meeting-intelligence-hub/
│
├── api/
│   └── main.py                 # FastAPI routes
│
├── services/
│   ├── ingestion.py            # Transcript parsing (.txt and .vtt)
│   ├── extractor.py            # LLM-powered decision & action extraction
│   ├── query_engine.py         # Chatbot query answering
│   └── exporter.py             # CSV and PDF export
│
├── models/
│   └── schema.py               # Pydantic response models
│
├── frontend/
│   └── app.py                  # Streamlit UI
│
├── sample_transcripts/
│   ├── test.txt                # Sample plain text transcript
│   └── test.vtt                # Sample WebVTT transcript
│
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🧪 Testing the Application

Sample transcripts are included in `sample_transcripts/` so you can test immediately after setup.

### Test Feature 1 — Extraction

1. Open `http://localhost:8501`
2. Go to the **Upload** tab
3. Upload `sample_transcripts/test.txt` or `sample_transcripts/test.vtt`
4. Go to the **Decisions & Actions** tab
5. View extracted decisions and action items
6. Click **Export as CSV** or **Export as PDF**

### Test Feature 2 — Chatbot

1. Upload a transcript first
2. Go to the **Chatbot** tab
3. Ask a question like:
   - _"When are we launching the product?"_
   - _"What did Sarah say she would do?"_
   - _"What budget decision was made?"_

---

## 🔌 API Endpoints

| Method | Endpoint   | Description                      |
| ------ | ---------- | -------------------------------- |
| GET    | `/`        | Health check                     |
| POST   | `/process` | Upload and process a transcript  |
| POST   | `/query`   | Ask a question about transcripts |

### Example — Process a transcript

```bash
curl -X POST http://localhost:8000/process \
  -F "file=@sample_transcripts/test.txt"
```

### Example — Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "When are we launching?", "transcript_text": "John: We decided to launch on the 15th."}'
```

---

## 🛡️ Error Handling

- Unsupported file types return a clear error message
- API failures retry automatically with exponential backoff
- Empty or malformed transcripts return empty results gracefully — the app never crashes

---

## 📬 Contact

Jerome Mathew
GitHub: [jeromemathew2004](https://github.com/jeromemathew2004)
