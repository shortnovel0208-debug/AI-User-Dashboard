"""
AI 心智监测看板 - 最小 Demo 后端
"""
import json
import os
import sqlite3
from collections import defaultdict

from flask import Flask, g, jsonify, render_template, request

APP_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(APP_DIR, "dashboard.db")

app = Flask(__name__, template_folder="templates", static_folder="static")


STANCE_LABELS = {
    "anxiety": {
        "anxious": "焦虑/担忧",
        "optimistic": "乐观",
        "balanced": "中立/理性",
        "dismissive": "不以为然",
    },
    "kids_learn": {
        "still_code": "仍应学编程",
        "ai_literacy": "应学 AI 素养",
        "humanities_critical": "人文/批判思维优先",
        "fundamentals_math": "数学/底层学科优先",
        "no_code_needed": "不必学编程",
    },
}

AUTHOR_LABELS = {
    "kol": "意见领袖 KOL",
    "tech": "科技从业者",
    "parent": "家长",
    "general": "普通用户",
}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db:
        db.close()


def month_key(date_str: str) -> str:
    return date_str[:7]  # yyyy-mm


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/meta")
def api_meta():
    return jsonify({
        "stance_labels": STANCE_LABELS,
        "author_labels": AUTHOR_LABELS,
    })


@app.route("/api/posts")
def api_posts():
    """支持筛选：topic / region / author_type / verified。"""
    topic = request.args.get("topic")
    region = request.args.get("region")
    author_type = request.args.get("author_type")
    verified = request.args.get("verified")  # "0" "1" or None

    sql = "SELECT * FROM posts WHERE 1=1"
    params = []
    if topic:
        sql += " AND topic=?"
        params.append(topic)
    if region:
        sql += " AND region=?"
        params.append(region)
    if author_type:
        sql += " AND author_type=?"
        params.append(author_type)
    if verified in ("0", "1"):
        sql += " AND human_verified=?"
        params.append(int(verified))
    sql += " ORDER BY posted_at DESC"

    rows = get_db().execute(sql, params).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/trends")
def api_trends():
    """按月聚合 stance 数，按 topic × region × author_type 分组。"""
    topic = request.args.get("topic", "anxiety")
    region = request.args.get("region")          # 可选
    author_type = request.args.get("author_type")  # 可选

    sql = "SELECT posted_at, stance, region, author_type FROM posts WHERE topic=?"
    params = [topic]
    if region:
        sql += " AND region=?"
        params.append(region)
    if author_type:
        sql += " AND author_type=?"
        params.append(author_type)

    rows = get_db().execute(sql, params).fetchall()

    # series: { stance: { month: count } }
    series = defaultdict(lambda: defaultdict(int))
    months = set()
    for r in rows:
        m = month_key(r["posted_at"])
        months.add(m)
        series[r["stance"]][m] += 1

    month_list = sorted(months)
    out = {
        "months": month_list,
        "stances": {
            st: [series[st].get(m, 0) for m in month_list]
            for st in series
        },
    }
    return jsonify(out)


@app.route("/api/compare")
def api_compare():
    """EN vs CN 对比：按月分别计算各 stance 的百分比占比。"""
    topic = request.args.get("topic", "kids_learn")
    rows = get_db().execute(
        "SELECT posted_at, stance, region FROM posts WHERE topic=?",
        (topic,),
    ).fetchall()

    # by_region: { region: { month: { stance: count } } }
    by_region = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    months = set()
    for r in rows:
        m = month_key(r["posted_at"])
        months.add(m)
        by_region[r["region"]][m][r["stance"]] += 1

    month_list = sorted(months)
    result = {"months": month_list, "regions": {}}
    for region, per_month in by_region.items():
        stance_series = defaultdict(list)
        for m in month_list:
            counts = per_month.get(m, {})
            total = sum(counts.values()) or 1
            for st in STANCE_LABELS.get(topic, {}):
                stance_series[st].append(round(100 * counts.get(st, 0) / total, 1))
        result["regions"][region] = dict(stance_series)
    return jsonify(result)


@app.route("/api/review", methods=["POST"])
def api_review():
    """人工审核写回：支持修正 stance / topic / author_type / region，并标记 verified。"""
    data = request.get_json(force=True)
    post_id = data.get("id")
    if not post_id:
        return jsonify({"error": "id required"}), 400

    allowed = ["topic", "stance", "author_type", "region", "human_notes"]
    updates = {k: data[k] for k in allowed if k in data}
    updates["human_verified"] = 1

    sets = ", ".join(f"{k}=?" for k in updates)
    params = list(updates.values()) + [post_id]
    db = get_db()
    db.execute(f"UPDATE posts SET {sets} WHERE id=?", params)
    db.commit()

    row = db.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()
    return jsonify(dict(row))


@app.route("/api/stats")
def api_stats():
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    verified = db.execute("SELECT COUNT(*) FROM posts WHERE human_verified=1").fetchone()[0]
    # AI vs Human 覆写率
    overrides = db.execute("""
        SELECT COUNT(*) FROM posts
        WHERE human_verified=1
          AND ai_labels_json IS NOT NULL
          AND json_extract(ai_labels_json,'$.stance') != stance
    """).fetchone()[0]
    return jsonify({
        "total": total,
        "verified": verified,
        "unverified": total - verified,
        "stance_overrides": overrides,
    })


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("DB not found, run: python seed_data.py")
    app.run(host="0.0.0.0", port=5000, debug=True)
