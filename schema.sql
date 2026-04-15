-- AI 心智监测看板 - 最小 Demo Schema
-- 每条记录 = 一条社媒原帖/评论，已打 AI 标签，可人工审核覆写

CREATE TABLE IF NOT EXISTS posts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source          TEXT NOT NULL,       -- reddit / mumsnet / zhihu / xiaohongshu / weibo / bilibili / wechat / douyin / unesco 等
    region          TEXT NOT NULL,       -- 'CN' 或 'EN'
    author_type     TEXT NOT NULL,       -- kol / tech / parent / general  (可人工再修正)
    topic           TEXT NOT NULL,       -- 'anxiety' (AI焦虑) / 'kids_learn' (孩子学什么/编程)
    stance          TEXT NOT NULL,       -- 见下方立场标签
    original_text   TEXT NOT NULL,       -- 原文（公开片段）
    translation     TEXT,                -- 英→中或中→英翻译，便于跨区对比
    url             TEXT,                -- 原帖/评论链接（占位或真实）
    posted_at       TEXT NOT NULL,       -- ISO 日期 (yyyy-mm-dd)
    ai_confidence   REAL DEFAULT 0.8,    -- AI 标注置信度
    ai_labels_json  TEXT,                -- 原始 AI 标签 JSON（用于对比人工修正）
    human_verified  INTEGER DEFAULT 0,   -- 0=未审 1=已审
    human_notes     TEXT                 -- 审核备注
);

-- 立场候选：
-- topic=anxiety:   anxious / optimistic / balanced / dismissive
-- topic=kids_learn: still_code / ai_literacy / humanities_critical / fundamentals_math / no_code_needed
