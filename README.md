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

- **Decision & Action Item Extractor** — Automatically identifies decisions made and tasks assigned from any meeting transcript with LLM-powered extraction
- **Multi-format Support** — Accepts both `.txt` and `.vtt` (WebVTT) transcript formats
- **Confidence Filtering** — Filter extracted decisions and action items by confidence threshold to focus on high-certainty findings
- **Contextual Query Chatbot** — Ask natural language questions across uploaded transcripts and get instant AI-powered answers
- **Speaker Sentiment & Tone Analysis** — Analyze sentiment for individual speakers and track emotional tone throughout meetings
- **Executive Summary Generator** — Generate AI-powered summaries for individual transcripts
- **Multi-Transcript Support** — Upload and analyze multiple transcripts simultaneously; the chatbot and sentiment analyzer work across all transcripts
- **Dashboard Statistics** — Real-time metrics showing total transcripts, decisions, action items, and word count
- **Export Options** — Download decisions and action items as CSV or PDF reports
- **Chat History Management** — Persistent chat history with clear functionality for conversation management
- **Professional UI** — Drag-and-drop upload, tabbed interface, styled cards, and responsive design

---

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
│   └── main.py                 # FastAPI routes and endpoints
│
├── services/
│   ├── ingestion.py            # Transcript parsing (.txt and .vtt)
│   ├── extractor.py            # LLM-powered decision & action extraction
│   ├── query_engine.py         # Chatbot query answering
│   ├── sentiment.py            # Speaker sentiment and tone analysis
│   ├── summarizer.py           # Executive summary generation
│   └── exporter.py             # CSV and PDF export
│
├── models/
│   └── schema.py               # Pydantic response models
│
├── frontend/
│   └── app.py                  # Streamlit multi-tab UI
│
├── sample_transcripts/
│   ├── test.txt                # Sample plain text transcript
│   ├── test.vtt                # Sample WebVTT transcript
│   ├── product_meeting.txt     # Additional sample transcript
│   └── ...                     # More sample transcripts
│
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── APPROACH.md                 # Technical approach document
```

---

## 🧪 Testing the Application

Sample transcripts are included in `sample_transcripts/` so you can test immediately after setup.

### Test Feature 1 — Decision & Action Item Extraction

1. Open `http://localhost:8501`
2. Go to the **📤 Upload Transcripts** tab
3. Upload `sample_transcripts/test.txt` or `sample_transcripts/test.vtt`
4. View processing status and transcript preview
5. Go to the **📋 Insights & Analytics** tab
6. View extracted decisions and action items with confidence scores
7. Use the **🎯 Filter by Confidence** slider to filter results
8. Export as CSV or PDF using the download buttons

### Test Feature 2 — Executive Summary

1. In the **📤 Upload Transcripts** tab, after uploading a transcript
2. Click the **✨ Generate Executive Summary** button
3. Wait for the AI to generate a summary
4. View the summary in the expanded transcript card

### Test Feature 3 — AI Chatbot

1. Upload a transcript first (in the **📤 Upload Transcripts** tab)
2. Go to the **💬 AI Assistant** tab
3. Ask questions like:
   - _"What were the main decisions made?"_
   - _"Who has action items assigned to them?"_
   - _"When are we launching the product?"_
   - _"What topics were discussed most?"_
4. Chat history is automatically maintained within the session
5. Click **🗑️ Clear Chat** to reset conversation

### Test Feature 4 — Sentiment Analysis

1. Upload a transcript first
2. Go to the **🎭 Sentiment Analysis** tab
3. Click **🔍 Analyse Sentiment**
4. View the sentiment timeline showing emotional arc throughout the meeting
5. See speaker sentiment breakdown showing each participant's average sentiment
6. Inspect individual segment details with full text passages

### Test Feature 5 — Multi-Transcript Support

1. Upload multiple transcripts in the **📤 Upload Transcripts** tab
2. In the **💬 AI Assistant** tab, the chatbot will search across all transcripts
3. In the **📋 Insights & Analytics** tab, view aggregated decisions and actions from all files
4. The sidebar dashboard shows combined statistics across all uploads

---

## 🔌 API Endpoints

| Method | Endpoint     | Description                      |
| ------ | ------------ | -------------------------------- |
| GET    | `/`          | Health check                     |
| POST   | `/process`   | Upload and process a transcript  |
| POST   | `/query`     | Ask a question about transcripts |
| POST   | `/sentiment` | Analyze sentiment for speakers   |
| POST   | `/summarize` | Generate executive summary       |

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

### Example — Sentiment Analysis

```bash
curl -X POST http://localhost:8000/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "John: Great work! Sarah: Thanks, excited to continue.", "speakers": ["John", "Sarah"]}'
```

### Example — Generate Summary

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "[full transcript text]", "filename": "meeting.txt"}'
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
