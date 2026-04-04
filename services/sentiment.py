import os
import re
from groq import Groq
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str, speakers: list) -> dict:
    """
    Full sentiment analysis pipeline:
    - Segment level sentiment (every N lines)
    - Speaker level sentiment breakdown
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    segments = _build_segments(lines)
    segment_results = _analyze_segments(segments)
    speaker_results = _analyze_speakers(lines, speakers)

    return {
        "segments": segment_results,
        "speakers": speaker_results,
        "overall": _overall_sentiment(segment_results)
    }


def _build_segments(lines: list, segment_size: int = 5) -> list:
    """Group lines into segments of N lines each."""
    segments = []
    for i in range(0, len(lines), segment_size):
        chunk = lines[i:i + segment_size]
        segments.append({
            "index": i // segment_size + 1,
            "lines": chunk,
            "text": "\n".join(chunk),
            "line_start": i + 1,
            "line_end": min(i + segment_size, len(lines))
        })
    return segments


def _analyze_segments(segments: list) -> list:
    """Run VADER on each segment, use Groq for ambiguous ones."""
    results = []

    for seg in segments:
        scores = analyzer.polarity_scores(seg["text"])
        compound = scores["compound"]

        if -0.2 <= compound <= 0.2:
            label = _classify_with_groq(seg["text"])
        elif compound > 0.2:
            label = "Consensus" if compound > 0.5 else "Positive"
        else:
            label = "Conflict" if compound < -0.5 else "Concern"

        results.append({
            "index": seg["index"],
            "text": seg["text"],
            "line_start": seg["line_start"],
            "line_end": seg["line_end"],
            "compound": round(compound, 3),
            "label": label,
            "color": _label_to_color(label)
        })

    return results


def _classify_with_groq(text: str) -> str:
    """Use Groq to classify ambiguous segments."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """Classify the sentiment of this meeting transcript segment into exactly one of these labels:
Consensus, Enthusiasm, Uncertainty, Concern, Conflict.
Respond with ONLY the label — nothing else."""
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0,
            max_tokens=10
        )
        label = response.choices[0].message.content.strip()
        valid = ["Consensus", "Enthusiasm", "Uncertainty", "Concern", "Conflict"]
        return label if label in valid else "Uncertainty"
    except Exception:
        return "Uncertainty"


def _analyze_speakers(lines: list, speakers: list) -> list:
    """Calculate average sentiment per speaker."""
    speaker_scores = {s: [] for s in speakers}

    for line in lines:
        if ":" in line:
            speaker = line.split(":")[0].strip()
            content = line.split(":", 1)[1].strip()
            if speaker in speaker_scores:
                score = analyzer.polarity_scores(content)["compound"]
                speaker_scores[speaker].append(score)

    results = []
    for speaker, scores in speaker_scores.items():
        if scores:
            avg = round(sum(scores) / len(scores), 3)
            results.append({
                "speaker": speaker,
                "average_sentiment": avg,
                "label": _score_to_label(avg),
                "color": _label_to_color(_score_to_label(avg)),
                "utterance_count": len(scores)
            })

    return sorted(results, key=lambda x: x["average_sentiment"], reverse=True)


def _score_to_label(score: float) -> str:
    if score > 0.5:
        return "Consensus"
    elif score > 0.2:
        return "Positive"
    elif score > -0.2:
        return "Uncertainty"
    elif score > -0.5:
        return "Concern"
    else:
        return "Conflict"


def _label_to_color(label: str) -> str:
    colors = {
        "Consensus": "#10b981",
        "Enthusiasm": "#3b82f6",
        "Positive": "#10b981",
        "Uncertainty": "#f59e0b",
        "Concern": "#f97316",
        "Conflict": "#ef4444"
    }
    return colors.get(label, "#94a3b8")


def _overall_sentiment(segments: list) -> dict:
    if not segments:
        return {"score": 0, "label": "Uncertainty", "color": "#f59e0b"}
    avg = sum(s["compound"] for s in segments) / len(segments)
    label = _score_to_label(avg)
    return {
        "score": round(avg, 3),
        "label": label,
        "color": _label_to_color(label)
    }