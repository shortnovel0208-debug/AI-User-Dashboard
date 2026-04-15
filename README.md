# 🧠 AI 心智监测看板 (Minimal Demo)

追踪社媒上对两个议题的心态迁移：
1. **AI 是否带来了越来越多的焦虑？**
2. **AI 时代，孩子还要不要学编程 / 应该学什么？**

并做 **中国 vs 英语国家** 的时间对比，验证「英语圈观点半年后是否在中文圈复现」。

## 能力

| 模块 | 说明 |
|---|---|
| 趋势 | 立场（anxious / optimistic / still_code / ai_literacy …）按月聚合时序折线 |
| 中英对比 | 同议题下中 / 英两地区立场占比堆叠柱 |
| 观点 & 原文 | 按立场分组列出用户原文（中英互译），每条带 source + url |
| 人工审核 | 审核 AI 打的 topic / stance / author_type / region，支持修正写回并统计覆写次数 |

## 数据源（Demo 覆盖的占位）

Reddit (r/Parenting / r/education / r/MachineLearning) · Mumsnet · 知乎 · 小红书 · 微博 · 哔哩哔哩 · 微信公众号 · 抖音 · OECD · Common Sense Media · 教育部。

> 本 Demo 的原文样本是从公开讨论中观察到的典型观点的 **代表性节选 / 复述**，用于演示看板结构。生产版本应由定向爬虫 + 人工采样管线直写入库（schema 已就绪）。

## 用户分层

kol（意见领袖） / tech（科技从业者） / parent（家长） / general（普通用户）——人工审核时可修正。

## 快速启动

```bash
pip install -r requirements.txt
python seed_data.py       # 构建 SQLite + 注入 35 条样本
python app.py             # http://127.0.0.1:5000
```

## 文件结构

```
app.py              Flask 后端 + API (/api/trends /api/compare /api/posts /api/review /api/stats)
schema.sql          SQLite 表结构（含 AI 原始标签 + 人工覆写字段）
seed_data.py        样本数据注入
templates/index.html
static/dashboard.js   前端（Chart.js）
static/style.css
```

## 扩展清单（下一步）

- 接入真实采集：Reddit API / Mumsnet RSS / 知乎问答抓取 / 微博关键词流
- 用 LLM 自动打 topic + stance + author_type 标签（落 `ai_labels_json` + `ai_confidence`）
- 审核队列按置信度从低到高优先排序
- 新增「细分论点演化」视图（同一立场下的关键词 diff）
- 接 UNESCO / OECD / 教育部政策文本做外部对照时间轴
