import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime


UA = "offline-dashboard-demo/1.0 (public data fetch; contact: example@example.com)"


def http_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def norm_date(date_str: str) -> str:
    if not date_str:
        return ""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return date_str
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except Exception:
        return str(date_str)[:10]


def pick_topic(text: str) -> str:
    t = (text or "").lower()
    kids = re.search(r"\b(kid|kids|child|children|parent|school|teacher|education|learn|learning|curriculum)\b", t)
    code = re.search(r"\b(code|coding|program|programming|scratch|python|cs|computer science)\b", t)
    anx = re.search(r"\b(anxiety|anxious|panic|fear|worried|worry|doom|job|jobs|career|layoff|unemploy|replace)\b", t)
    if (kids or code) and not anx:
        return "kids_learn"
    if anx and not (kids or code):
        return "anxiety"
    if kids or code:
        return "kids_learn"
    return "anxiety"


def pick_author_type(source: str, context: str) -> str:
    s = (source or "").lower()
    c = (context or "").lower()
    if s == "reddit":
        if "parenting" in c or "dad" in c or "mom" in c:
            return "parent"
        if "machinelearning" in c or "cscareerquestions" in c or "learnprogramming" in c:
            return "tech"
    if s == "hn":
        return "tech"
    return "general"


def stance_anxiety(text: str) -> tuple[str, float]:
    t = (text or "").lower()
    anxious = len(re.findall(r"\b(anxiety|anxious|panic|fear|worried|worry|hopeless|terrified|doom)\b", t))
    dismiss = len(re.findall(r"\b(overhyped|marketing|bullshit|bs|calm down|not real|can't|hallucinat)\b", t))
    optim = len(re.findall(r"\b(optimistic|excited|opportunity|adapt|fine|better|benefit)\b", t))
    bal = len(re.findall(r"\b(rational|nuance|balance|tradeoff|limit|cautious|mixed)\b", t))
    scores = {"anxious": anxious, "dismissive": dismiss, "optimistic": optim, "balanced": bal}
    best = max(scores, key=scores.get)
    top = scores[best]
    if top == 0:
        return "balanced", 0.35
    conf = min(0.95, 0.45 + 0.12 * top)
    return best, conf


def stance_kids(text: str) -> tuple[str, float]:
    t = (text or "").lower()
    no_code = len(re.findall(r"\b(no need to code|don'?t need to code|coding is dead|stop teaching code)\b", t))
    still_code = len(re.findall(r"\b(should learn to code|still learn to code|teach.*code|learn programming|coding teaches)\b", t))
    ai_lit = len(re.findall(r"\b(ai literacy|prompt|prompting|verify|verification|ethic|ethics|tool)\b", t))
    humanities = len(re.findall(r"\b(critical thinking|humanities|writing|reading|debate|communication|media literacy|empathy)\b", t))
    math = len(re.findall(r"\b(math|mathematics|stats|statistics|probability|linear algebra)\b", t))
    scores = {
        "no_code_needed": no_code,
        "still_code": still_code,
        "ai_literacy": ai_lit,
        "humanities_critical": humanities,
        "fundamentals_math": math,
    }
    best = max(scores, key=scores.get)
    top = scores[best]
    if top == 0:
        return "ai_literacy", 0.3
    conf = min(0.95, 0.45 + 0.12 * top)
    return best, conf


def label_post(text: str) -> tuple[str, str, float]:
    topic = pick_topic(text)
    if topic == "anxiety":
        st, conf = stance_anxiety(text)
    else:
        st, conf = stance_kids(text)
    return topic, st, conf


def fetch_reddit(query: str, subreddits: list[str], limit: int):
    out = []
    per = min(100, limit)
    for sr in subreddits:
        q = urllib.parse.quote(query)
        url = f"https://www.reddit.com/r/{sr}/search.json?q={q}&restrict_sr=1&sort=new&limit={per}&t=all"
        try:
            data = http_json(url)
        except Exception:
            time.sleep(1.0)
            continue
        for ch in (data.get("data", {}) or {}).get("children", []) or []:
            d = ch.get("data") or {}
            title = d.get("title") or ""
            selftext = d.get("selftext") or ""
            text = (title + "\n" + selftext).strip()
            if not text:
                continue
            out.append({
                "source": "reddit",
                "region": "REDDIT",
                "context": f"r/{sr}",
                "title": title,
                "text": text,
                "posted_at": datetime.utcfromtimestamp(d.get("created_utc") or time.time()).strftime("%Y-%m-%d"),
                "url": "https://www.reddit.com" + (d.get("permalink") or ""),
            })
        time.sleep(1.1)
        if len(out) >= limit:
            break
    return out[:limit]


def fetch_hn(query: str, limit: int):
    q = urllib.parse.quote(query)
    out = []
    page = 0
    while len(out) < limit and page < 10:
        url = f"https://hn.algolia.com/api/v1/search?query={q}&tags=story&page={page}&hitsPerPage=50"
        data = http_json(url)
        hits = data.get("hits") or []
        if not hits:
            break
        for h in hits:
            title = h.get("title") or ""
            story_url = h.get("url") or ("https://news.ycombinator.com/item?id=" + str(h.get("objectID")))
            extra = h.get("story_text") or h.get("comment_text") or ""
            text = (title + "\n" + extra).strip() if extra else title
            out.append({
                "source": "hn",
                "region": "HN",
                "context": "Hacker News",
                "title": title,
                "text": text,
                "posted_at": norm_date(h.get("created_at")),
                "url": story_url,
            })
            if len(out) >= limit:
                break
        page += 1
        time.sleep(0.35)
    return out[:limit]


def dedupe(items: list[dict]):
    seen = set()
    out = []
    for it in items:
        key = (it.get("url") or "").strip()
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def build_posts(target_total: int = 100):
    anxiety_queries = [
        "ai anxiety",
        "ai job loss",
        "ai replacing jobs",
        "ai layoffs",
        "automation anxiety",
        "future of work ai",
    ]
    kids_queries = [
        "kids learn programming",
        "teach kids coding",
        "ai literacy education",
        "ai in schools",
        "should kids learn to code",
        "education and ai",
    ]

    raw = []
    for q in anxiety_queries:
        raw.extend(fetch_hn(q, limit=80))
    for q in kids_queries:
        raw.extend(fetch_hn(q, limit=80))
    raw = dedupe(raw)

    labeled = []
    for it in raw:
        topic, stance, conf = label_post(it.get("text") or "")
        author_type = pick_author_type(it.get("source"), it.get("context"))
        labeled.append((topic, {
            "source": it.get("source"),
            "region": it.get("region"),
            "author_type": author_type,
            "topic": topic,
            "stance": stance,
            "posted_at": it.get("posted_at"),
            "original_text": it.get("title") or it.get("text") or "",
            "translation": "",
            "url": it.get("url"),
            "human_verified": 0,
            "human_notes": "",
            "ai_confidence": round(float(conf), 2),
            "ai_labels_json": json.dumps(
                {"topic": topic, "stance": stance, "author_type": author_type, "region": it.get("region")},
                ensure_ascii=False,
            ),
        }))

    anxiety = [p for t, p in labeled if t == "anxiety"]
    kids = [p for t, p in labeled if t == "kids_learn"]

    anxiety_cap = target_total // 2
    kids_cap = target_total - anxiety_cap
    picked = anxiety[:anxiety_cap] + kids[:kids_cap]
    if len(picked) < target_total:
        rest = anxiety[anxiety_cap:] + kids[kids_cap:]
        picked.extend(rest[: (target_total - len(picked))])

    posts = []
    for idx, p in enumerate(picked, start=1):
        p["id"] = idx
        posts.append(p)
    return posts


def main():
    posts = build_posts(target_total=100)
    with open("real_posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(posts)} posts to real_posts.json")


if __name__ == "__main__":
    main()
