import argparse
import json


def replace_posts_block(html: str) -> str:
    start = html.find("const POSTS = [")
    if start < 0:
        raise RuntimeError("POSTS block start not found")
    end = html.find("];", start)
    if end < 0:
        raise RuntimeError("POSTS block end not found")
    end += 2
    return (
        html[:start]
        + 'const POSTS = JSON.parse(document.getElementById("posts-data").textContent);\n'
        + html[end:]
    )


def insert_posts_json(html: str, posts_json: str) -> str:
    needle = "\n  <script>\n"
    idx = html.find(needle)
    if idx < 0:
        raise RuntimeError("main script tag not found")
    insert = f'\n  <script id="posts-data" type="application/json">{posts_json}</script>\n'
    return html[:idx] + insert + html[idx:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default="/workspace/offline_dashboard.html")
    ap.add_argument("--posts", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", default="Offline")
    ap.add_argument("--title", default="AI 心智监测看板 · Offline")
    args = ap.parse_args()

    with open(args.template, "r", encoding="utf-8") as f:
        html = f.read()
    with open(args.posts, "r", encoding="utf-8") as f:
        posts = json.load(f)
    posts_json = json.dumps(posts, ensure_ascii=False, separators=(",", ":"))

    html = html.replace("AI 心智监测看板 · Offline", args.title)
    html = html.replace('<span class="tag">Offline</span>', f'<span class="tag">{args.label}</span>')
    html = html.replace(
        "离线静态版：内置样本数据，可直接双击打开，不依赖后端服务。",
        f"离线静态版：内置 {len(posts)} 条样本数据，可直接双击打开，不依赖后端服务。",
    )
    html = html.replace("本离线版内置样本数据用于演示。", f"本离线版内置 {len(posts)} 条样本数据用于演示。")

    html = replace_posts_block(html)
    html = insert_posts_json(html, posts_json)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main()

