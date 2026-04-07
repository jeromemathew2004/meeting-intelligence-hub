# Approach Document — Meeting Intelligence Hub

**Cymonic Technologies — Campus Recruitment 2026**
Jerome Mathew

---

## Solution Design

The Meeting Intelligence Hub is a two-tier application — a FastAPI backend and a Streamlit frontend — that transforms raw meeting transcripts into structured, queryable intelligence.

The core pipeline works in four stages:

1. **Ingestion** — Uploaded transcripts are parsed and cleaned by a format-aware ingestion service that handles both plain text and WebVTT files, extracting speaker labels and text segments.

2. **Extraction** — The cleaned text is sent to a large language model (Llama 3.3 via Groq) with a strict system prompt that enforces structured JSON output — extracting decisions, action items, assignees, deadlines, and confidence scores for each extraction.

3. **Analysis** — The same transcript content is simultaneously processed for speaker sentiment and emotional tone analysis, producing per-speaker metrics and segment-level sentiment scores.

4. **Querying** — A retrieval-augmented chatbot interface allows natural language questions to be answered by the LLM using the full transcript context, enabling users to get specific information on demand.

The system is designed around a single principle: **the API layer should always return a valid response**. Every LLM call is wrapped in retry logic with exponential backoff, and a fallback handler ensures the application never crashes due to an external API failure. Empty results are handled gracefully across all features.

---

## Tech Stack Choices

**FastAPI** was chosen for the backend because it provides automatic request validation via Pydantic, auto-generated Swagger documentation, and async support — all with minimal boilerplate. This made it easy to build and test each endpoint independently before wiring up the frontend.

**Streamlit** was chosen for the frontend because it allows a fully functional, multi-page UI to be built entirely in Python. For a project of this scope and timeline, eliminating the JavaScript layer was the right trade-off. Streamlit's built-in components — file uploader, chat interface, dataframes, and download buttons — covered every UI requirement in the brief.

**Groq API with Llama 3.3 70B** was chosen as the LLM provider because it offers a genuinely free tier with no credit card required, making the application immediately accessible to any evaluator without setup friction. The model performs at a level comparable to GPT-4o-mini for structured extraction tasks, and the OpenAI-compatible API interface made integration straightforward.

**ReportLab** was used for PDF generation because it gives precise control over table layout and styling, producing a professional output without external dependencies.

---

## Key Design Decisions

**Structured output enforcement.** Rather than parsing free-form LLM responses, the system prompt explicitly defines the required JSON schema and instructs the model to return nothing else. A post-processing step strips any markdown fences the model adds despite the instruction. This two-layer approach makes the extraction pipeline robust against the most common LLM output inconsistencies.

**Confidence scoring for filtering.** Each extracted decision and action item receives a confidence score (0-1) directly from the LLM based on how certain it is about the extraction. This enables users to apply a confidence threshold slider to filter out low-certainty extractions and focus on high-confidence findings. The filtering is applied on the frontend, allowing users to interactively explore results at different confidence levels without re-running the backend.

**Session-based state management.** The Streamlit frontend manages all application state using `st.session_state`, enabling persistent chat history, transcript storage, and filter settings within a user session. This approach simplifies the backend (keeping it stateless) while providing a rich interactive experience on the frontend. The sidebar dashboard leverages session state to display real-time aggregated statistics across uploaded transcripts.

**Separation of concerns.** Each service — ingestion, extraction, querying, sentiment analysis, and export — is an independent module with a single responsibility. This makes each component testable in isolation and easy to swap out. For example, replacing Groq with any other LLM provider requires changes to only one file (`extractor.py`).

**Stateless API design.** The FastAPI backend is fully stateless — it processes each request independently and returns all results in the response. This design simplifies deployment and makes the backend horizontally scalable. Complex logic like multi-transcript aggregation happens on the frontend.

**Multi-transcript support throughout.** Rather than limiting users to a single transcript at a time, the architecture was designed from the start to handle multiple simultaneous uploads. The chatbot searches across all transcripts, the analytics tab aggregates decisions and actions from all files, and the sentiment analyzer can work on any selected transcript from the list.

---

## Implementation Highlights

**Confidence filtering without re-running the backend.** Since each extraction receives a confidence score from the LLM, filtering happens entirely on the frontend. When users adjust the confidence slider, the app instantly updates displayed results without making new API calls. This keeps the UX responsive and reduces unnecessary LLM invocations. Empty filter results are handled gracefully with informative messages rather than crashes.

**Error resilience through defensive programming.** The app handles edge cases like:

- Empty extracted lists (when no decisions or actions are found)
- DataFrame selection errors when column names don't match expected schema
- API failures with exponential backoff and informative error messages
- Missing metadata fields with sensible defaults
- Malformed transcripts with graceful degradation

**Session state for scalability.** Rather than storing results in the backend, state lives in Streamlit's session state. This means the backend remains stateless and can be horizontally scaled. Multiple users can use the app simultaneously without interfering with each other's sessions. Transcript aggregation and complex filtering logic runs client-side on the frontend.

**Structured API responses.** Every endpoint returns a Pydantic-validated response model with consistent structure. This makes the API contract clear, enables auto-generated Swagger docs, and catches response format errors early. If an LLM returns unexpected output, the Pydantic model fails loudly rather than silently accepting corrupt data.

---

## Features Implemented

Beyond the core requirements, the application includes several advanced features:

- **Confidence Filtering** — Interactive slider to filter extractions by confidence threshold
- **Sentiment Analysis** — Speaker-level sentiment analysis with emotional tone tracking throughout meetings
- **Executive Summary Generation** — AI-powered meeting summaries with fallback handling
- **Multi-Transcript Support** — Simultaneous analysis of multiple meeting transcripts with aggregated results
- **Dashboard Statistics** — Real-time metrics showing aggregate insights across uploaded transcripts
- **Chat History Management** — Persistent conversation history within the user session with clear functionality
- **Robust Error Handling** — Graceful degradation when filtering results in empty datasets; no crashes on API failures

---

## What I Would Improve With More Time

**Vector database for semantic search.** Currently the chatbot passes the full transcript text to the LLM on every query. With more time I would implement ChromaDB to chunk and embed transcripts, enabling semantic retrieval of only the most relevant sections before sending to the LLM. This would improve answer accuracy, reduce hallucinations, and enable the system to reliably scale to dozens of long transcripts without hitting token limits.

**Persistent storage layer.** Uploaded transcripts and extracted insights currently exist only in the Streamlit session and are lost on page refresh. Adding a lightweight database (SQLite or PostgreSQL) would allow users to build up a library of meetings over time, search historical transcripts, and generate reports comparing decisions or action items across different meetings.

**Speaker diarisation.** The current parser extracts speaker labels from manually labelled transcripts. Integrating a diarisation model like Whisper or Pyannote would enable the system to automatically identify speakers from raw audio files, completely removing the dependency on pre-formatted transcripts. This would dramatically improve user experience.

**Confidence score calibration.** The LLM-assigned confidence scores are currently uncalibrated. With more time I would build a small evaluation set of manually labelled transcripts, measure extraction precision and recall at different confidence thresholds, and use this analysis to fine-tune the system prompt and post-processing for higher accuracy.

**Real-time transcript processing.** The system could be extended to process live meeting transcripts (from APIs like Zoom, Teams, or Otter.ai) as they occur, providing real-time decision and action item extraction and alerts.

**Advanced export options.** Beyond CSV and PDF, adding exports to Jira (auto-create tickets for action items), Slack (post summaries), or Google Sheets (sync results) would integrate the tool deeper into existing team workflows.

---

_Document length: 2 pages_
