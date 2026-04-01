import json
import time
import os
from groq import Groq
from dotenv import load_dotenv
from models.schema import InsightItem, Insights

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert meeting analyst. Your job is to extract structured insights from meeting transcripts.

You must respond with ONLY valid JSON — no preamble, no explanation, no markdown code fences.

The JSON must match this exact structure:
{
  "decisions": [
    {
      "speaker": "Name of person who made or led the decision",
      "text": "The decision that was made, in full",
      "confidence": 0.85,
      "reason": ["why you classified this as a decision"]
    }
  ],
  "actions": [
    {
      "speaker": "Name of person assigned the task",
      "text": "The specific task or action item",
      "confidence": 0.80,
      "reason": ["why you classified this as an action item"]
    }
  ]
}

Rules:
- Decisions are things the team agreed on, concluded, or finalized
- Actions are tasks assigned to a specific person with an implied or explicit deadline
- confidence is a float between 0.0 and 1.0
- reason is a list of short strings explaining your classification
- If no decisions or actions exist, return empty lists
- Speaker should be "Unknown" if not identifiable
- Never invent information not present in the transcript"""


def extract_info(text: str) -> Insights:
    """
    Extract decisions and action items using Groq (free tier).
    Falls back to empty insights if the API call fails.
    """
    try:
        raw = _call_groq(text)
        print("[DEBUG] Groq raw response:", raw)
        return _parse_response(raw)
    except Exception as e:
        print(f"[Extractor] Groq call failed: {e}")
        return _fallback_insights()


def _call_groq(text: str) -> str:
    """Call Groq API with retry logic."""
    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Extract all decisions and action items from this transcript:\n\n{text}"}
                ],
                temperature=0.1,
                max_tokens=2048
            )
            return response.choices[0].message.content

        except Exception as e:
            last_error = e
            wait = 2 ** attempt
            print(f"[Extractor] Groq error on attempt {attempt + 1}: {e}")
            time.sleep(wait)

    raise last_error


def _parse_response(raw: str) -> Insights:
    """Parse and validate Groq's JSON response into Pydantic models."""
    cleaned = raw.strip()

    # Strip markdown fences if model added them
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1])

    data = json.loads(cleaned)

    decisions = [
        InsightItem(
            speaker=item.get("speaker", "Unknown"),
            text=item.get("text", ""),
            confidence=float(item.get("confidence", 0.5)),
            reason=item.get("reason", [])
        )
        for item in data.get("decisions", [])
    ]

    actions = [
        InsightItem(
            speaker=item.get("speaker", "Unknown"),
            text=item.get("text", ""),
            confidence=float(item.get("confidence", 0.5)),
            reason=item.get("reason", [])
        )
        for item in data.get("actions", [])
    ]

    return Insights(decisions=decisions, actions=actions)


def _fallback_insights() -> Insights:
    """Return empty insights if Groq is unreachable — never crash the API."""
    return Insights(decisions=[], actions=[])