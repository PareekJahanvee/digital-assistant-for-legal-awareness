from flask import Flask, render_template, request, abort
import json
import re
import os

app = Flask(__name__)

JSON_PATH = "categorized_constitution.json"


def load_data():
    """Load the JSON file – abort with a friendly message if it is missing."""
    if not os.path.exists(JSON_PATH):
        abort(
            500,
            description=(
                "categorized_constitution.json not found.<br><br>"
                "Run the preprocessing steps first:<br>"
                "<code>python preprocess.py</code><br>"
                "<code>python categorize.py</code>"
            ),
        )
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Load once when the module is imported
DATA = load_data()


def highlight(text: str, terms: list[str]) -> str:
    """Wrap every search term with <mark>…</mark>."""
    if not terms:
        return text
    pattern = "|".join(re.escape(t) for t in terms)
    return re.sub(f"({pattern})", r"<mark>\1</mark>", text, flags=re.IGNORECASE)


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    sel_cat = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        sel_cat = request.form.get("category", "").strip()
        words = [w.lower() for w in query.split() if w]

        for art in DATA:
            title = art["title"]
            text = art["text"]
            cat = art["category"]

            # ---- query match (any word) ----
            q_match = not words or any(
                w in title.lower() or w in text.lower() for w in words
            )

            # ---- category filter ----
            c_match = not sel_cat or sel_cat.lower() == cat.lower()

            if q_match and c_match:
                highlighted = highlight(text, words)
                results.append(
                    {"title": title, "text": highlighted, "category": cat}
                )

    # Dynamic <datalist>
    all_cats = sorted({a["category"] for a in DATA})

    return render_template(
        "index.html",
        results=results,
        query=query,
        selected_category=sel_cat,
        categories=all_cats,
    )

if __name__ == "__main__":
    # debug=True gives nice error pages in the browser
    app.run(host="0.0.0.0", port=5000, debug=True)
