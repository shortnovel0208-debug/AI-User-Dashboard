import json


def replace_posts_block(html: str) -> str:
    start = html.find("const POSTS = [")
    if start < 0:
        raise RuntimeError("POSTS block start not found")
    end = html.find("];", start)
    if end < 0:
        raise RuntimeError("POSTS block end not found")
    end += 2
    return html[:start] + 'const POSTS = JSON.parse(document.getElementById("posts-data").textContent);\n' + html[end:]


def insert_posts_json(html: str, posts_json: str) -> str:
    needle = "\n  <script>\n"
    idx = html.find(needle)
    if idx < 0:
        raise RuntimeError("main script tag not found")
    insert = f'\n  <script id="posts-data" type="application/json">{posts_json}</script>\n'
    return html[:idx] + insert + html[idx:]


def main():
    with open("/workspace/offline_dashboard.html", "r", encoding="utf-8") as f:
        html = f.read()
    with open("/workspace/posts_500.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
    posts_json = json.dumps(posts, ensure_ascii=False, separators=(",", ":"))

    html = html.replace("AI 心智监测看板 · Offline", "AI 心智监测看板 · Offline 500")
    html = html.replace('<span class="tag">Offline</span>', '<span class="tag">Offline 500</span>')
    html = html.replace(
        "离线静态版：内置样本数据，可直接双击打开，不依赖后端服务。",
        "离线静态版：内置 500 条样本数据，可直接双击打开，不依赖后端服务。",
    )
    html = html.replace("本离线版内置样本数据用于演示。", "本离线版内置 500 条样本数据用于演示。")

    html = replace_posts_block(html)
    html = insert_posts_json(html, posts_json)

    with open("/workspace/offline_dashboard_500.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main()

