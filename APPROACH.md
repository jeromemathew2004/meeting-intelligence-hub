# Approach Document — Meeting Intelligence Hub

**Cymonic Technologies — Campus Recruitment 2026**
Jerome Mathew

---

## Solution Design

The Meeting Intelligence Hub is a two-tier application — a FastAPI backend and a Streamlit frontend — that transforms raw meeting transcripts into structured, queryable intelligence.

The core pipeline works in three stages. First, uploaded transcripts are parsed and cleaned by a format-aware ingestion service that handles both plain text and WebVTT files. Second, the cleaned text is sent to a large language model with a strict system prompt that enforces structured JSON output — extracting decisions, action items, assignees, deadlines, and confidence scores. Third, the same transcript content is made available to a retrieval-augmented chatbot that answers natural language questions with cited sources.

The system is designed around a single principle: the API layer should always return a valid response. Every LLM call is wrapped in retry logic with exponential backoff, and a fallback handler ensures the application never crashes due to an external API failure.

---

## Tech Stack Choices

**FastAPI** was chosen for the backend because it provides automatic request validation via Pydantic, auto-generated Swagger documentation, and async support — all with minimal boilerplate. This made it easy to build and test each endpoint independently before wiring up the frontend.

**Streamlit** was chosen for the frontend because it allows a fully functional, multi-page UI to be built entirely in Python. For a project of this scope and timeline, eliminating the JavaScript layer was the right trade-off. Streamlit's built-in components — file uploader, chat interface, dataframes, and download buttons — covered every UI requirement in the brief.

**Groq API with Llama 3.3 70B** was chosen as the LLM provider because it offers a genuinely free tier with no credit card required, making the application immediately accessible to any evaluator without setup friction. The model performs at a level comparable to GPT-4o-mini for structured extraction tasks, and the OpenAI-compatible API interface made integration straightforward.

**ReportLab** was used for PDF generation because it gives precise control over table layout and styling, producing a professional output without external dependencies.

---

## Key Design Decisions

**Structured output enforcement.** Rather than parsing free-form LLM responses, the system prompt explicitly defines the required JSON schema and instructs the model to return nothing else. A post-processing step strips any markdown fences the model adds despite the instruction. This two-layer approach makes the extraction pipeline robust against the most common LLM output inconsistencies.

**Separation of concerns.** Each service — ingestion, extraction, querying, and export — is an independent module with a single responsibility. This makes each component testable in isolation and easy to swap out. For example, replacing Groq with any other LLM provider requires changes to only one file.

**Stateless API design.** The FastAPI backend is fully stateless — it processes each request independently and returns all results in the response. State is managed entirely on the frontend in Streamlit's session state. This simplifies deployment and makes the backend horizontally scalable.

---

## What I Would Improve With More Time

**Vector database for semantic search.** Currently the chatbot passes the full transcript text to the LLM on every query. With more time I would implement ChromaDB to chunk and embed transcripts, enabling semantic retrieval of only the most relevant sections. This would improve answer accuracy and allow the system to scale to dozens of long transcripts without hitting token limits.

**Speaker diarisation for .vtt files.** The current parser extracts speaker labels from manually labelled transcripts. Integrating a diarisation model like Whisper would enable the system to automatically identify speakers from raw audio, removing the dependency on pre-labelled transcripts.

**Persistent storage.** Uploaded transcripts currently exist only in the Streamlit session and are lost on refresh. Adding a lightweight database like SQLite would allow users to build up a library of meetings over time and query across their entire meeting history.

**Confidence score calibration.** The LLM-assigned confidence scores are currently uncalibrated. With more time I would build a small evaluation set of manually labelled transcripts to measure extraction precision and recall, and use this to fine-tune the system prompt for higher accuracy.

---

_Document length: 2 pages_
