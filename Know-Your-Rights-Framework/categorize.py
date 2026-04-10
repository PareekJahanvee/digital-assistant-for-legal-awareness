import json
from typing import List
CATEGORY_KEYWORDS = {
    "Fundamental Rights": ["freedom", "equality", "liberty", "religion", "expression", "right"],
    "Citizenship": ["citizen", "citizenship", "migration", "nationality"],
    "Judiciary": ["court", "judge", "justice", "supreme court", "high court"],
    "Women's Rights": ["women", "gender", "discrimination", "empowerment"],
    "Labour Laws": ["labour", "employment", "wages", "worker", "factory"],
    "Education Laws": ["education", "school", "university", "literacy"],
    "Government Structure": ["president", "parliament", "prime minister", "union", "state"],
    "Emergency Provisions": ["emergency", "proclamation", "suspension"],
}
def categorize(input_json: str = "constitution_clean.json",
               output_json: str = "categorized_constitution.json") -> List[dict]:
    with open(input_json, "r", encoding="utf-8") as f:
        articles = json.load(f)
    out = []
    for art in articles:
        txt = art["text"].lower()
        cat = "Uncategorized"
        for name, kws in CATEGORY_KEYWORDS.items():
            if any(k in txt for k in kws):
                cat = name
                break
        out.append({
            "title": art["title"],
            "text": art["text"],         
            "category": cat
        })
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Categorized {len(out)} articles → {output_json}")
    return out
if __name__ == "__main__":
    categorize()
