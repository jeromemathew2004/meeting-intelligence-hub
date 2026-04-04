import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert meeting analyst. Generate a concise executive summary of the meeting transcript provided.

You must respond with ONLY valid JSON — no preamble, no explanation, no markdown code fences.

The JSON must match this exact structure:
{
    "headline": "One sentence capturing the core purpose of this meeting",
    "summary": "3-5 sentence executive summary of what was discussed and decided",
    "key_topics": ["topic 1", "topic 2", "topic 3"],
    "mood": "Overall mood of the meeting in one word e.g. Productive, Tense, Enthusiastic, Collaborative",
    "next_steps": "One sentence describing what happens after this meeting"
}

Rules:
- headline must be under 15 words
- summary must be 3-5 sentences maximum
- key_topics must be 3-5 short topics
- mood must be a single word
- next_steps must be under 20 words
- Never invent information not in the transcript"""


def generate_summary(text: str, filename: str) -> dict:
    """Generate an executive summary of a meeting transcript."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate an executive summary for this meeting transcript from {filename}:\n\n{text}"}
            ],
            temperature=0.1,
            max_tokens=512
        )
        raw = response.choices[0].message.content.strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1])

        import json
        data = json.loads(raw)
        return {
            "headline": data.get("headline", "Meeting Summary"),
            "summary": data.get("summary", ""),
            "key_topics": data.get("key_topics", []),
            "mood": data.get("mood", "Neutral"),
            "next_steps": data.get("next_steps", "")
        }

    except Exception as e:
        print(f"[Summarizer] Error: {e}")
        return {
            "headline": "Summary unavailable",
            "summary": "Could not generate summary. Please try again.",
            "key_topics": [],
            "mood": "Unknown",
            "next_steps": ""
        }