# preprocess.py
import pdfplumber
import json
import re
from pathlib import Path

def clean_page(text: str) -> str:
    """Remove page numbers, headers, footers, and normalize whitespace."""
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        # Skip page numbers, "Page X", etc.
        if re.fullmatch(r"\d+", line) or line.lower().startswith("page"):
            continue
        if len(line) < 3:
            continue
        lines.append(line)
    return re.sub(r"\s+", " ", " ".join(lines)).strip()

def extract_articles(pdf_path: str) -> list[dict]:
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            raw = page.extract_text()
            if raw:
                full_text += "\n" + clean_page(raw)

    full_text = re.sub(r'\s+', ' ', full_text)
    full_text = re.sub(r'(ARTICLE\s+\d+[A-Z]*[.:]?)', r'\n\1', full_text, flags=re.IGNORECASE)
    full_text = full_text.strip()

    splitter = re.compile(r"\bARTICLE\s+(\d+[A-Z]*)(?:[.:])?", re.IGNORECASE)
    parts = splitter.split(full_text)

    i = 1
    while i < len(parts):
        number_part = parts[i].strip()  # e.g., "14", "21A"
        body = parts[i + 1] if i + 1 < len(parts) else ""

        title = f"Article {number_part}"

        # Cut body at the next article header
        next_match = splitter.search(body)
        if next_match:
            body = body[:next_match.start()].strip()
        else:
            body = body.strip()

        # Final cleanup: collapse any remaining multiple spaces
        body = re.sub(r"\s+", " ", body).strip()

        if title and body:
            data.append({"title": title, "text": body})

        i += 2

    return data


def save_json(data: list[dict], out_path: str):
    Path(out_path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Saved {len(data)} articles to {out_path}")


if __name__ == "__main__":
    articles = extract_articles("Constitution_of_India.pdf")
    save_json(articles, "constitution_clean.json")
