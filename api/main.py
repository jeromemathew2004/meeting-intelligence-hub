from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from services.ingestion import parse_transcript
from services.extractor import extract_info
from models.schema import ProcessedResponse

app = FastAPI()


@app.get("/")
def root():
    return {"status": "Meeting Intelligence Hub API running"}


@app.post("/process")
async def process_file(file: UploadFile):

    if not file.filename.endswith((".txt", ".vtt")):
        raise HTTPException(status_code=400, detail="Only .txt and .vtt files supported")

    content = await file.read()
    text = content.decode("utf-8")

    parsed = parse_transcript(text)
    extracted = extract_info(parsed["clean_text"])

    return {
        "metadata": {
            "word_count": parsed["word_count"],
            "line_count": parsed["line_count"],
            "char_count": parsed["char_count"],
            "clean_text": parsed["clean_text"],  # ← THIS was missing
            "speakers": parsed.get("speakers", []),
            "meeting_date": parsed.get("meeting_date", "Unknown")
        },
        "insights": extracted
    }
 

class QueryRequest(BaseModel):
    question: str
    transcript_text: str


@app.post("/query")
async def query(request: QueryRequest):
    from services.query_engine import answer_question
    answer = answer_question(request.question, request.transcript_text)
    return {"answer": answer}