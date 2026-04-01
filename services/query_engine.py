import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert meeting analyst assistant. 
You are given the content of one or more meeting transcripts and a question about them.

Answer the question accurately based ONLY on the transcript content provided.
Always cite your source by mentioning the meeting filename and the speaker.

Format your answer clearly. If the answer is not in the transcripts, say so honestly.
Never make up information."""


def answer_question(question: str, transcript_text: str) -> str:
    """Answer a natural language question about the transcript content."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Transcripts:\n\n{transcript_text}\n\nQuestion: {question}"}
            ],
            temperature=0.1,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[QueryEngine] Error: {e}")
        return "I encountered an error while searching the transcripts. Please try again."