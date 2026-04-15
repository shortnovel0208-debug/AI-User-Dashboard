"""
Seed 脚本 - 为最小 Demo 注入代表性样本数据。

说明：
- 样本是从公开讨论中观察到的典型观点的「代表性复述 / 节选」，
  用来演示看板能力。生产版本应由爬虫 + 人工采样管线直接落库。
- 每条样本都带有 url 占位（real_url_placeholder），可替换为真实链接。
- 时间跨度 2025-09 ~ 2026-04，便于展示「英语圈观点半年后在中文圈复现」的对比假设。
"""
import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "dashboard.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


SAMPLES = [
    # ============ EN / anxiety ============
    dict(source="reddit", region="EN", author_type="parent", topic="anxiety",
         stance="anxious", posted_at="2025-09-12",
         original_text="I genuinely don't know what jobs will exist when my 8yo grows up. Every week another profession looks disrupted. I'm losing sleep over this.",
         translation="我真的不知道我 8 岁孩子长大后还有什么工作。每周都有新职业被颠覆，为此我睡不好觉。",
         url="https://reddit.com/r/Parenting/example_ai_anxiety_1"),
    dict(source="mumsnet", region="EN", author_type="parent", topic="anxiety",
         stance="anxious", posted_at="2025-10-03",
         original_text="AITA for feeling hopeless about my kids' future careers? Teachers keep saying 'they'll be fine' but have they seen GPT-5 lately?",
         translation="我对孩子未来职业感到绝望是不是过度了？老师都说「他们没事的」，但他们看过最新的 GPT-5 吗？",
         url="https://mumsnet.com/Talk/example_ai_anxiety_2"),
    dict(source="reddit", region="EN", author_type="tech", topic="anxiety",
         stance="balanced", posted_at="2025-10-18",
         original_text="Worked in ML for 12 years. The hype cycle is real but so is the disruption. Long-term I'm cautiously optimistic, short-term it's going to be messy for mid-skill jobs.",
         translation="做 ML 12 年了。炒作是真的，冲击也是真的。长期我谨慎乐观，短期中等技能岗位会很痛。",
         url="https://reddit.com/r/MachineLearning/example_ai_anxiety_3"),
    dict(source="reddit", region="EN", author_type="kol", topic="anxiety",
         stance="optimistic", posted_at="2025-11-02",
         original_text="Every tech revolution caused panic. Web, mobile, cloud. AI is bigger but humans will adapt like we always did. Stop doomposting.",
         translation="每次技术革命都引发恐慌。Web、移动、云端。AI 更大，但人类像以往一样会适应。别再唱衰。",
         url="https://x.com/example_kol_ai_anxiety_4"),
    dict(source="mumsnet", region="EN", author_type="parent", topic="anxiety",
         stance="anxious", posted_at="2025-12-15",
         original_text="My teenager is spiraling. Says there's no point studying anything because AI will do it. I don't know how to respond.",
         translation="我十几岁的孩子开始崩溃，说学什么都没意义因为 AI 都能做。我不知道怎么回应。",
         url="https://mumsnet.com/Talk/example_teen_anxiety"),
    dict(source="reddit", region="EN", author_type="general", topic="anxiety",
         stance="dismissive", posted_at="2026-01-22",
         original_text="It's all marketing. These 'agents' still can't book a flight without hallucinating. Calm down.",
         translation="全是营销。这些「智能体」订个机票都会乱编。冷静一下。",
         url="https://reddit.com/r/artificial/example_dismissive"),
    dict(source="reddit", region="EN", author_type="tech", topic="anxiety",
         stance="balanced", posted_at="2026-02-09",
         original_text="Anxiety is rational, paralysis isn't. Use AI, understand its limits, re-skill where needed. Anxiety without action is just stress.",
         translation="焦虑是理性的，瘫痪不是。用 AI、理解它的边界、必要时再培训。焦虑不行动只是压力。",
         url="https://reddit.com/r/cscareerquestions/example_balanced"),
    dict(source="reddit", region="EN", author_type="parent", topic="anxiety",
         stance="optimistic", posted_at="2026-03-11",
         original_text="Honestly I've become less anxious over time. My kid uses AI to learn faster than I ever could. We just need to teach judgement.",
         translation="说实话我越来越不焦虑了。孩子用 AI 学得比我以前快得多。我们只需要教他判断力。",
         url="https://reddit.com/r/Parenting/example_optimistic"),

    # ============ CN / anxiety ============
    dict(source="zhihu", region="CN", author_type="parent", topic="anxiety",
         stance="balanced", posted_at="2025-10-20",
         original_text="说不焦虑是假的，但焦虑没用。身边同事孩子都在卷 AI 夏令营，我们家暂时先练阅读和表达。",
         translation="It's a lie to say I'm not anxious, but anxiety is useless. My colleagues' kids are all in AI summer camps; we focus on reading and communication for now.",
         url="https://zhihu.com/question/example_cn_anxiety_1"),
    dict(source="xiaohongshu", region="CN", author_type="parent", topic="anxiety",
         stance="anxious", posted_at="2025-11-15",
         original_text="看了扎克伯格说要裁掉中级工程师，我连夜把孩子的 Python 课退了，又报了新的 AI 产品经理课。谁能告诉我该学什么？😭",
         translation="After seeing Zuckerberg say they'll lay off mid-level engineers, I cancelled my kid's Python course overnight and signed up for an AI PM course instead. Can anyone tell me what to learn?",
         url="https://xiaohongshu.com/discovery/example_cn_anxiety_2"),
    dict(source="weibo", region="CN", author_type="kol", topic="anxiety",
         stance="optimistic", posted_at="2025-12-08",
         original_text="每次技术革命都会有一波焦虑，然后一波新机会。家长与其焦虑，不如和孩子一起学 AI 工具，这是我家的做法。",
         translation="Every tech revolution comes with anxiety then new opportunities. Instead of being anxious, learn AI tools together with your kids — that's what we do.",
         url="https://weibo.com/example_cn_kol_anxiety"),
    dict(source="bilibili", region="CN", author_type="general", topic="anxiety",
         stance="anxious", posted_at="2026-01-18",
         original_text="刚毕业找不到工作，看着 AI 一个比一个强，每天都在怀疑读这么多年书的意义。",
         translation="Just graduated can't find a job, AI getting stronger every day, questioning the meaning of all those years of schooling.",
         url="https://bilibili.com/video/example_cn_grad_anxiety"),
    dict(source="wechat", region="CN", author_type="kol", topic="anxiety",
         stance="balanced", posted_at="2026-02-20",
         original_text="与其问「AI会不会替代人」，不如问「哪些场景仍然需要人的判断和责任」。焦虑的背面是行动。",
         translation="Instead of asking 'will AI replace people', ask 'which scenarios still need human judgment and accountability'. The flip side of anxiety is action.",
         url="https://mp.weixin.qq.com/s/example_cn_balanced"),
    dict(source="douyin", region="CN", author_type="parent", topic="anxiety",
         stance="anxious", posted_at="2026-03-05",
         original_text="连小学老师都在用 AI 批作业了，我们家孩子以后拿什么竞争？真的想躺平。",
         translation="Even elementary teachers grade with AI now. What will my kid compete with later? I really want to give up.",
         url="https://douyin.com/video/example_cn_anxiety_3"),
    dict(source="zhihu", region="CN", author_type="tech", topic="anxiety",
         stance="balanced", posted_at="2026-03-28",
         original_text="作为算法工程师，真心建议家长别短线焦虑。让孩子会提问、会判断、会协作，比现在学什么具体技术重要得多。",
         translation="As an ML engineer, I honestly advise parents not to be short-term anxious. Teaching kids to ask, judge, and collaborate matters far more than any specific tech.",
         url="https://zhihu.com/answer/example_cn_tech_balanced"),

    # ============ EN / kids_learn ============
    dict(source="reddit", region="EN", author_type="tech", topic="kids_learn",
         stance="still_code", posted_at="2025-09-20",
         original_text="Coding teaches decomposition and debugging. Those skills are MORE valuable when AI writes the code, not less. Kids should still learn to code.",
         translation="编程教会分解问题和 debug。当 AI 写代码时，这些技能更有价值，而不是更没价值。孩子还是要学编程。",
         url="https://reddit.com/r/learnprogramming/example_en_still_code"),
    dict(source="reddit", region="EN", author_type="kol", topic="kids_learn",
         stance="ai_literacy", posted_at="2025-10-11",
         original_text="Hot take: syntax-level coding classes for 10yos are obsolete. Teach prompting, verification, and AI ethics instead.",
         translation="观点：给 10 岁孩子教语法级编程已经过时了。应该教 prompt、验证和 AI 伦理。",
         url="https://x.com/example_en_kol_literacy"),
    dict(source="mumsnet", region="EN", author_type="parent", topic="kids_learn",
         stance="humanities_critical", posted_at="2025-11-05",
         original_text="We pivoted our daughter from Scratch to debate club. Critical thinking & writing will outlast any language or framework.",
         translation="我们让女儿从 Scratch 转到辩论社。批判性思维和写作能比任何语言框架活得都久。",
         url="https://mumsnet.com/Talk/example_en_humanities"),
    dict(source="reddit", region="EN", author_type="parent", topic="kids_learn",
         stance="fundamentals_math", posted_at="2025-12-02",
         original_text="Math and stats are the real moat. If kids understand probability and linear algebra, AI is a tool; if not, AI is a black box.",
         translation="数学和统计才是真正的护城河。孩子懂概率和线代，AI 就是工具；不懂，AI 就是黑盒子。",
         url="https://reddit.com/r/education/example_en_math"),
    dict(source="reddit", region="EN", author_type="tech", topic="kids_learn",
         stance="ai_literacy", posted_at="2026-01-08",
         original_text="I work at a FAANG. We hire for taste and problem framing now. Kids should build stuff with AI, not memorize syntax.",
         translation="我在 FAANG。我们现在招人看审美和问题拆解。孩子应该用 AI 做东西，而不是背语法。",
         url="https://reddit.com/r/cscareerquestions/example_en_literacy_2"),
    dict(source="mumsnet", region="EN", author_type="parent", topic="kids_learn",
         stance="still_code", posted_at="2026-02-14",
         original_text="My 14yo built a Discord bot with Copilot last weekend. He learned MORE about coding than his whole term at school. Coding isn't dead — it's democratized.",
         translation="我 14 岁的娃用 Copilot 周末就写了个 Discord 机器人，比学校一学期学的还多。编程没死，而是被民主化了。",
         url="https://mumsnet.com/Talk/example_en_still_code_2"),
    dict(source="reddit", region="EN", author_type="general", topic="kids_learn",
         stance="no_code_needed", posted_at="2026-03-01",
         original_text="Why would anyone teach a kid to code when they can just describe what they want? Save them the pain.",
         translation="AI 都能描述即得，为什么还要教孩子写代码？别让他们受罪了。",
         url="https://reddit.com/r/artificial/example_en_no_code"),
    dict(source="reddit", region="EN", author_type="kol", topic="kids_learn",
         stance="humanities_critical", posted_at="2026-03-22",
         original_text="The scarce skill in 2030 won't be coding — it'll be asking the right questions and owning the consequences. Raise kids who can do that.",
         translation="2030 年稀缺的不是编程，而是会提对问题、敢承担后果。把孩子培养成这样的人。",
         url="https://x.com/example_en_kol_humanities"),
    dict(source="oecd", region="EN", author_type="kol", topic="kids_learn",
         stance="ai_literacy", posted_at="2026-02-01",
         original_text="Future-ready curricula should combine computational thinking with AI literacy and socio-emotional skills.",
         translation="面向未来的课程应结合计算思维、AI 素养和社会情感能力。",
         url="https://oecd.org/education/example_ai_literacy_report"),

    # ============ CN / kids_learn ============
    dict(source="zhihu", region="CN", author_type="tech", topic="kids_learn",
         stance="still_code", posted_at="2025-10-15",
         original_text="让孩子学编程不是为了写代码，是为了学分解问题。AI 时代这个能力更重要。Python 还是要学。",
         translation="Teaching kids coding isn't about writing code but learning decomposition. This matters more in the AI era. Python still needs to be learned.",
         url="https://zhihu.com/answer/example_cn_still_code"),
    dict(source="xiaohongshu", region="CN", author_type="parent", topic="kids_learn",
         stance="still_code", posted_at="2025-11-12",
         original_text="朋友说 AI 来了编程没用，但我家坚持每周 Scratch 一小时。逻辑思维这东西别的课替代不了。",
         translation="My friend said coding is useless once AI came, but we still do Scratch one hour a week. Nothing else replaces logical thinking.",
         url="https://xiaohongshu.com/discovery/example_cn_still_code"),
    dict(source="weibo", region="CN", author_type="kol", topic="kids_learn",
         stance="humanities_critical", posted_at="2025-12-18",
         original_text="AI 时代最稀缺的是提问能力、审美和同理心，这些都需要阅读和讨论来培养，不是刷编程题。",
         translation="The scarcest skills in the AI era are asking questions, taste, and empathy — these come from reading and discussion, not coding drills.",
         url="https://weibo.com/example_cn_kol_humanities"),
    dict(source="bilibili", region="CN", author_type="tech", topic="kids_learn",
         stance="ai_literacy", posted_at="2026-01-05",
         original_text="我在大厂带 AI 团队，我女儿的「编程课」现在是和 AI 一起做小游戏。教语法没意义，教她怎么用 AI + 验证结果才有用。",
         translation="I lead an AI team at a big tech firm. My daughter's 'coding class' is now building games with AI. Teaching syntax is pointless; teaching her to use AI and verify results matters.",
         url="https://bilibili.com/video/example_cn_ai_literacy"),
    dict(source="wechat", region="CN", author_type="kol", topic="kids_learn",
         stance="ai_literacy", posted_at="2026-02-12",
         original_text="家长问我还要不要给孩子报编程班。我的建议：把一半时间换成 AI 素养课——prompt、事实核查、伦理判断。",
         translation="Parents ask if kids should still take coding classes. My advice: swap half the time for AI literacy — prompting, fact-checking, ethical judgment.",
         url="https://mp.weixin.qq.com/s/example_cn_kol_literacy"),
    dict(source="zhihu", region="CN", author_type="parent", topic="kids_learn",
         stance="fundamentals_math", posted_at="2026-02-25",
         original_text="我是理工妈，坚决认为数学物理比编程更底层。AI 工具每年换一套，数学一辈子不换。",
         translation="I'm a STEM mom. Math and physics are more fundamental than coding. AI tools change yearly; math is for life.",
         url="https://zhihu.com/answer/example_cn_math"),
    dict(source="xiaohongshu", region="CN", author_type="parent", topic="kids_learn",
         stance="humanities_critical", posted_at="2026-03-10",
         original_text="我家今年把编程课停了，换成了阅读俱乐部和辩论。原因很简单：代码 AI 写得比孩子好，但提问和思辨它不会。",
         translation="We stopped the coding class this year and switched to a book club and debate. Reason: AI writes code better than kids, but it can't ask questions or think critically.",
         url="https://xiaohongshu.com/discovery/example_cn_humanities"),
    dict(source="douyin", region="CN", author_type="general", topic="kids_learn",
         stance="no_code_needed", posted_at="2026-03-18",
         original_text="现在写代码 AI 一句话就搞定，还让孩子学啥编程？学点赚钱的实际技能不香吗。",
         translation="AI writes code in one sentence now. Why make kids learn coding? Learn something practical that makes money.",
         url="https://douyin.com/video/example_cn_no_code"),
    dict(source="wechat", region="CN", author_type="kol", topic="kids_learn",
         stance="ai_literacy", posted_at="2026-04-02",
         original_text="新一年趋势很清楚：从「学编程」转向「学与 AI 协作」。重点不是写代码，是会评估 AI 输出。",
         translation="The trend this year is clear: from 'learn to code' to 'learn to collaborate with AI'. The point isn't writing code — it's evaluating AI output.",
         url="https://mp.weixin.qq.com/s/example_cn_trend_2026"),
    dict(source="moe_cn", region="CN", author_type="kol", topic="kids_learn",
         stance="ai_literacy", posted_at="2026-01-30",
         original_text="推进中小学人工智能教育，构建面向未来的人机协作素养课程体系。",
         translation="Promote AI education in primary/secondary schools; build a future-facing human-AI collaboration curriculum.",
         url="http://moe.gov.cn/example_policy"),
    dict(source="commonsense", region="EN", author_type="kol", topic="kids_learn",
         stance="humanities_critical", posted_at="2026-01-14",
         original_text="Parents should prioritize media literacy and critical evaluation of AI output over tool-specific skills.",
         translation="家长应把媒介素养和 AI 输出的批判性评估放在工具技能之前。",
         url="https://commonsensemedia.org/example_ai_guide"),
]


def main():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)

    for s in SAMPLES:
        ai_labels = {
            "topic": s["topic"],
            "stance": s["stance"],
            "author_type": s["author_type"],
            "region": s["region"],
        }
        conn.execute(
            """INSERT INTO posts
               (source, region, author_type, topic, stance, original_text,
                translation, url, posted_at, ai_confidence, ai_labels_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (s["source"], s["region"], s["author_type"], s["topic"], s["stance"],
             s["original_text"], s.get("translation"), s.get("url"),
             s["posted_at"], 0.8, json.dumps(ai_labels, ensure_ascii=False)),
        )

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    conn.close()
    print(f"Seeded {count} posts into {DB_PATH}")


if __name__ == "__main__":
    main()
