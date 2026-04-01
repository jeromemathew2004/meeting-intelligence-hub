def parse_transcript(text: str):
    lines = [l for l in text.split("\n") if l.strip()]
    words = text.split()

    return {
        "word_count": len(words),
        "line_count": len(lines),
        "char_count": len(text),
        "clean_text": text.strip()
    }