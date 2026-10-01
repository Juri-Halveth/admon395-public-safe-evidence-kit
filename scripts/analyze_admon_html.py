from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "evidence" / "Suchergebnisse_admon395_PAGE1_PUBLIC_SAFE.html"


def clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


raw = HTML.read_bytes()
text = raw.decode("utf-8", errors="replace")
soup = BeautifulSoup(text, "html.parser")

summary_line = clean(soup.select_one("#searchbits").find_previous(string=True) or "") if soup.select_one("#searchbits") else ""

results = []
for li in soup.select("ol#searchbits > li"):
    li_text = clean(li.get_text(" ", strip=True))
    h2 = li.find("h2")
    topic_a = h2.find("a") if h2 else None
    topic = clean(topic_a.get_text(" ", strip=True)) if topic_a else None
    topic_url = topic_a.get("href") if topic_a else None
    post_id = li.get("id")
    post_a = None
    for a in li.find_all("a", href=True):
        href = a["href"]
        if "#post" in href or "?p=" in href:
            post_a = a
            break
    post_title = clean(post_a.get_text(" ", strip=True)) if post_a else None
    post_url = post_a.get("href") if post_a else None
    # Drop common chrome and keep a compact excerpt near the post link.
    excerpt = li_text
    for marker in ["Thema:", "von admon395"]:
        excerpt = excerpt.replace(marker, " ")
    excerpt = clean(excerpt)
    results.append(
        {
            "post_id": post_id,
            "topic": topic,
            "topic_url": topic_url,
            "post_title": post_title,
            "post_url": post_url,
            "text": excerpt,
        }
    )

words = re.findall(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]{2,}", " ".join(r["text"] for r in results).lower())
stop = {
    "und", "oder", "der", "die", "das", "ich", "ist", "ein", "eine", "einen", "einem", "mit",
    "von", "auf", "im", "im", "in", "zu", "zum", "zur", "den", "dem", "des", "dass", "nicht",
    "mir", "mich", "war", "als", "wie", "für", "seit", "nur", "wenn", "auch", "man", "mal",
    "thema", "admon395", "beiträge", "antworten", "hits", "letzter", "beitrag", "forum",
}
counter = Counter(w for w in words if w not in stop)

topics = Counter(r["topic"] for r in results)
theme_terms = [
    "traum", "träum", "schlaf", "schlafparalyse", "gestalt", "schwarz", "stimme",
    "zahlen", "codes", "wand", "dejavu", "vorhersage", "astral", "sterben",
    "erinnerung", "sprache", "zauberei", "latein", "sohn", "baby", "oma", "rot",
]
hits = defaultdict(list)
for r in results:
    hay = (r["topic"] + " " + r["post_title"] + " " + r["text"]).lower()
    for term in theme_terms:
        if term in hay:
            hits[term].append(r["post_id"])

out = {
    "title": clean(soup.title.get_text()) if soup.title else None,
    "summary_text": clean(soup.select_one("div.searchstats, .searchstats").get_text(" ", strip=True)) if soup.select_one("div.searchstats, .searchstats") else None,
    "result_count_page": len(results),
    "repeated_topics": {k: v for k, v in topics.items() if v > 1},
    "top_words": counter.most_common(50),
    "theme_hits": {k: len(v) for k, v in sorted(hits.items())},
    "results": results,
}

print(json.dumps(out, ensure_ascii=False, indent=2))
