import re
from models.schema import Metadata
import re
from datetime import datetime

def _detect_date(text: str, filename: str) -> str:
    """Try to detect meeting date from filename or transcript content."""

    # Try filename first — e.g. 2026-04-03_meeting.txt or meeting_20260403.txt
    date_patterns_filename = [
        r'(\d{4}-\d{2}-\d{2})',   # 2026-04-03
        r'(\d{4}\d{2}\d{2})',      # 20260403
        r'(\d{2}-\d{2}-\d{4})',   # 03-04-2026
    ]
    for pattern in date_patterns_filename:
        match = re.search(pattern, filename)
        if match:
            return match.group(1)

    # Try transcript content — look for common date formats
    date_patterns_content = [
        r'\b(\d{4}-\d{2}-\d{2})\b',                          # 2026-04-03
        r'\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\b',         # 03/04/2026
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # April 3, 2026
        r'\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',    # 3 April 2026
    ]
    for pattern in date_patterns_content:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

    # Fall back to today's date
    return datetime.today().strftime("%Y-%m-%d")


def parse_transcript(text: str) -> dict:
    """Auto-detect format and parse .txt or .vtt transcript."""
    if _is_vtt(text):
        return _parse_vtt(text)
    else:
        return _parse_txt(text)


def _is_vtt(text: str) -> bool:
    """Check if the text is a WebVTT file."""
    return text.strip().startswith("WEBVTT")


def _parse_txt(text: str) -> dict:
    """Parse plain text transcript."""
    clean = text.strip()
    lines = [l.strip() for l in clean.split("\n") if l.strip()]
    speakers = _extract_speakers(lines)

    return {
        "word_count": len(clean.split()),
        "line_count": len(lines),
        "char_count": len(clean),
        "clean_text": clean,
        "speakers": speakers,
        "format": "txt",
        "meeting_date": _detect_date(clean, "")
    }


def _parse_vtt(text: str) -> dict:
    """Parse WebVTT transcript — extracts timestamps and speaker labels."""
    lines = text.strip().split("\n")
    dialogue_lines = []
    clean_lines = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip WEBVTT header, NOTE blocks, and timestamps
        if line == "WEBVTT" or line.startswith("NOTE"):
            i += 1
            continue

        # Detect timestamp lines like 00:00:10.000 --> 00:00:15.000
        if "-->" in line:
            i += 1
            # Next line(s) are the dialogue
            while i < len(lines) and lines[i].strip():
                dialogue = lines[i].strip()
                clean_lines.append(dialogue)
                dialogue_lines.append(dialogue)
                i += 1
            continue

        i += 1

    full_text = "\n".join(clean_lines)
    speakers = _extract_speakers(clean_lines)

    return {
        "word_count": len(full_text.split()),
        "line_count": len(clean_lines),
        "char_count": len(full_text),
        "clean_text": full_text,
        "speakers": speakers,
        "format": "vtt",
        "meeting_date": _detect_date(clean, "")
    }


def _extract_speakers(lines: list) -> list:
    """Extract unique speaker names from lines formatted as 'Speaker: text'."""
    speakers = set()
    for line in lines:
        if ":" in line:
            speaker = line.split(":")[0].strip()
            # Filter out timestamps and empty strings
            if speaker and not re.match(r'[\d:\.]+', speaker):
                speakers.add(speaker)
    return list(speakers)