import re
from models.schema import Metadata

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
        "format": "txt"
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
        "format": "vtt"
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