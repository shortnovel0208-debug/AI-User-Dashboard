import argparse
import json
import math


BASE_POSTS = [
    {
        "id": 1,
        "source": "reddit",
        "region": "EN",
        "author_type": "parent",
        "topic": "anxiety",
        "stance": "anxious",
        "posted_at": "2025-09-12",
        "original_text": "I genuinely don't know what jobs will exist when my 8yo grows up. Every week another profession looks disrupted. I'm losing sleep over this.",
        "translation": "我真的不知道我 8 岁孩子长大后还有什么工作。每周都有新职业被颠覆，为此我睡不好觉。",
        "url": "https://reddit.com/r/Parenting/example_ai_anxiety_1",
    },
    {
        "id": 2,
        "source": "mumsnet",
        "region": "EN",
        "author_type": "parent",
        "topic": "anxiety",
        "stance": "anxious",
        "posted_at": "2025-10-03",
        "original_text": "AITA for feeling hopeless about my kids' future careers? Teachers keep saying 'they'll be fine' but have they seen GPT-5 lately?",
        "translation": "我对孩子未来职业感到绝望是不是过度了？老师都说「他们没事的」，但他们看过最新的 GPT-5 吗？",
        "url": "https://mumsnet.com/Talk/example_ai_anxiety_2",
    },
    {
        "id": 3,
        "source": "reddit",
        "region": "EN",
        "author_type": "tech",
        "topic": "anxiety",
        "stance": "balanced",
        "posted_at": "2025-10-18",
        "original_text": "Worked in ML for 12 years. The hype cycle is real but so is the disruption. Long-term I'm cautiously optimistic, short-term it's going to be messy for mid-skill jobs.",
        "translation": "做 ML 12 年了。炒作是真的，冲击也是真的。长期我谨慎乐观，短期中等技能岗位会很痛。",
        "url": "https://reddit.com/r/MachineLearning/example_ai_anxiety_3",
    },
    {
        "id": 4,
        "source": "reddit",
        "region": "EN",
        "author_type": "kol",
        "topic": "anxiety",
        "stance": "optimistic",
        "posted_at": "2025-11-02",
        "original_text": "Every tech revolution caused panic. Web, mobile, cloud. AI is bigger but humans will adapt like we always did. Stop doomposting.",
        "translation": "每次技术革命都引发恐慌。Web、移动、云端。AI 更大，但人类像以往一样会适应。别再唱衰。",
        "url": "https://x.com/example_kol_ai_anxiety_4",
    },
    {
        "id": 5,
        "source": "mumsnet",
        "region": "EN",
        "author_type": "parent",
        "topic": "anxiety",
        "stance": "anxious",
        "posted_at": "2025-12-15",
        "original_text": "My teenager is spiraling. Says there's no point studying anything because AI will do it. I don't know how to respond.",
        "translation": "我十几岁的孩子开始崩溃，说学什么都没意义因为 AI 都能做。我不知道怎么回应。",
        "url": "https://mumsnet.com/Talk/example_teen_anxiety",
    },
    {
        "id": 6,
        "source": "reddit",
        "region": "EN",
        "author_type": "general",
        "topic": "anxiety",
        "stance": "dismissive",
        "posted_at": "2026-01-22",
        "original_text": "It's all marketing. These 'agents' still can't book a flight without hallucinating. Calm down.",
        "translation": "全是营销。这些「智能体」订个机票都会乱编。冷静一下。",
        "url": "https://reddit.com/r/artificial/example_dismissive",
    },
    {
        "id": 7,
        "source": "reddit",
        "region": "EN",
        "author_type": "tech",
        "topic": "anxiety",
        "stance": "balanced",
        "posted_at": "2026-02-09",
        "original_text": "Anxiety is rational, paralysis isn't. Use AI, understand its limits, re-skill where needed. Anxiety without action is just stress.",
        "translation": "焦虑是理性的，瘫痪不是。用 AI、理解它的边界、必要时再培训。焦虑不行动只是压力。",
        "url": "https://reddit.com/r/cscareerquestions/example_balanced",
    },
    {
        "id": 8,
        "source": "reddit",
        "region": "EN",
        "author_type": "parent",
        "topic": "anxiety",
        "stance": "optimistic",
        "posted_at": "2026-03-11",
        "original_text": "Honestly I've become less anxious over time. My kid uses AI to learn faster than I ever could. We just need to teach judgement.",
        "translation": "说实话我越来越不焦虑了。孩子用 AI 学得比我以前快得多。我们只需要教他判断力。",
        "url": "https://reddit.com/r/Parenting/example_optimistic",
    },
    {
        "id": 9,
        "source": "zhihu",
        "region": "CN",
        "author_type": "parent",
        "topic": "anxiety",
        "stance": "balanced",
        "posted_at": "2025-10-20",
        "original_text": "说不焦虑是假的，但焦虑没用。身边同事孩子都在卷 AI 夏令营，我们家暂时先练阅读和表达。",
        "translation": "It's a lie to say I'm not anxious, but anxiety is useless. My colleagues' kids are all in AI summer camps; we focus on reading and communication for now.",
        "url": "https://zhihu.com/question/example_cn_anxiety_1",
    },
    {
        "id": 10,
        "source": "xiaohongshu",
        "region": "CN",
        "author_type": "parent",
        "topic": "anxiety",
        "stance": "anxious",
        "posted_at": "2025-11-15",
        "original_text": "看了扎克伯格说要裁掉中级工程师，我连夜把孩子的 Python 课退了，又报了新的 AI 产品经理课。谁能告诉我该学什么？😭",
        "translation": "After seeing Zuckerberg say they'll lay off mid-level engineers, I cancelled my kid's Python course overnight and signed up for an AI PM course instead. Can anyone tell me what to learn?",
        "url": "https://xiaohongshu.com/discovery/example_cn_anxiety_2",
    },
    {
        "id": 11,
        "source": "weibo",
        "region": "CN",
        "author_type": "kol",
        "topic": "anxiety",
        "stance": "optimistic",
        "posted_at": "2025-12-08",
        "original_text": "每次技术革命都会有一波焦虑，然后一波新机会。家长与其焦虑，不如和孩子一起学 AI 工具，这是我家的做法。",
        "translation": "Every tech revolution comes with anxiety then new opportunities. Instead of being anxious, learn AI tools together with your kids — that's what we do.",
        "url": "https://weibo.com/example_cn_kol_anxiety",
    },
    {
        "id": 12,
        "source": "bilibili",
        "region": "CN",
        "author_type": "general",
        "topic": "anxiety",
        "stance": "anxious",
        "posted_at": "2026-01-18",
        "original_text": "刚毕业找不到工作，看着 AI 一个比一个强，每天都在怀疑读这么多年书的意义。",
        "translation": "Just graduated can't find a job, AI getting stronger every day, questioning the meaning of all those years of schooling.",
        "url": "https://bilibili.com/video/example_cn_grad_anxiety",
    },
    {
        "id": 13,
        "source": "wechat",
        "region": "CN",
        "author_type": "kol",
        "topic": "anxiety",
        "stance": "balanced",
        "posted_at": "2026-02-20",
        "original_text": "与其问「AI会不会替代人」，不如问「哪些场景仍然需要人的判断和责任」。焦虑的背面是行动。",
        "translation": "Instead of asking 'will AI replace people', ask 'which scenarios still need human judgment and accountability'. The flip side of anxiety is action.",
        "url": "https://mp.weixin.qq.com/s/example_cn_balanced",
    },
    {
        "id": 14,
        "source": "douyin",
        "region": "CN",
        "author_type": "parent",
        "topic": "anxiety",
        "stance": "anxious",
        "posted_at": "2026-03-05",
        "original_text": "连小学老师都在用 AI 批作业了，我们家孩子以后拿什么竞争？真的想躺平。",
        "translation": "Even elementary teachers grade with AI now. What will my kid compete with later? I really want to give up.",
        "url": "https://douyin.com/video/example_cn_anxiety_3",
    },
    {
        "id": 15,
        "source": "zhihu",
        "region": "CN",
        "author_type": "tech",
        "topic": "anxiety",
        "stance": "balanced",
        "posted_at": "2026-03-28",
        "original_text": "作为算法工程师，真心建议家长别短线焦虑。让孩子会提问、会判断、会协作，比现在学什么具体技术重要得多。",
        "translation": "As an ML engineer, I honestly advise parents not to be short-term anxious. Teaching kids to ask, judge, and collaborate matters far more than any specific tech.",
        "url": "https://zhihu.com/answer/example_cn_tech_balanced",
    },
    {
        "id": 16,
        "source": "reddit",
        "region": "EN",
        "author_type": "tech",
        "topic": "kids_learn",
        "stance": "still_code",
        "posted_at": "2025-09-20",
        "original_text": "Coding teaches decomposition and debugging. Those skills are MORE valuable when AI writes the code, not less. Kids should still learn to code.",
        "translation": "编程教会分解问题和 debug。当 AI 写代码时，这些技能更有价值，而不是更没价值。孩子还是要学编程。",
        "url": "https://reddit.com/r/learnprogramming/example_en_still_code",
    },
    {
        "id": 17,
        "source": "reddit",
        "region": "EN",
        "author_type": "kol",
        "topic": "kids_learn",
        "stance": "ai_literacy",
        "posted_at": "2025-10-11",
        "original_text": "Hot take: syntax-level coding classes for 10yos are obsolete. Teach prompting, verification, and AI ethics instead.",
        "translation": "观点：给 10 岁孩子教语法级编程已经过时了。应该教 prompt、验证和 AI 伦理。",
        "url": "https://x.com/example_en_kol_literacy",
    },
    {
        "id": 18,
        "source": "mumsnet",
        "region": "EN",
        "author_type": "parent",
        "topic": "kids_learn",
        "stance": "humanities_critical",
        "posted_at": "2025-11-05",
        "original_text": "We pivoted our daughter from Scratch to debate club. Critical thinking & writing will outlast any language or framework.",
        "translation": "我们让女儿从 Scratch 转到辩论社。批判性思维和写作能比任何语言框架活得都久。",
        "url": "https://mumsnet.com/Talk/example_en_humanities",
    },
    {
        "id": 19,
        "source": "reddit",
        "region": "EN",
        "author_type": "parent",
        "topic": "kids_learn",
        "stance": "fundamentals_math",
        "posted_at": "2025-12-02",
        "original_text": "Math and stats are the real moat. If kids understand probability and linear algebra, AI is a tool; if not, AI is a black box.",
        "translation": "数学和统计才是真正的护城河。孩子懂概率和线代，AI 就是工具；不懂，AI 就是黑盒子。",
        "url": "https://reddit.com/r/education/example_en_math",
    },
    {
        "id": 20,
        "source": "reddit",
        "region": "EN",
        "author_type": "tech",
        "topic": "kids_learn",
        "stance": "ai_literacy",
        "posted_at": "2026-01-08",
        "original_text": "I work at a FAANG. We hire for taste and problem framing now. Kids should build stuff with AI, not memorize syntax.",
        "translation": "我在 FAANG。我们现在招人看审美和问题拆解。孩子应该用 AI 做东西，而不是背语法。",
        "url": "https://reddit.com/r/cscareerquestions/example_en_literacy_2",
    },
    {
        "id": 21,
        "source": "mumsnet",
        "region": "EN",
        "author_type": "parent",
        "topic": "kids_learn",
        "stance": "still_code",
        "posted_at": "2026-02-14",
        "original_text": "My 14yo built a Discord bot with Copilot last weekend. He learned MORE about coding than his whole term at school. Coding isn't dead — it's democratized.",
        "translation": "我 14 岁的娃用 Copilot 周末就写了个 Discord 机器人，比学校一学期学的还多。编程没死，而是被民主化了。",
        "url": "https://mumsnet.com/Talk/example_en_still_code_2",
    },
    {
        "id": 22,
        "source": "reddit",
        "region": "EN",
        "author_type": "general",
        "topic": "kids_learn",
        "stance": "no_code_needed",
        "posted_at": "2026-03-01",
        "original_text": "Why would anyone teach a kid to code when they can just describe what they want? Save them the pain.",
        "translation": "AI 都能描述即得，为什么还要教孩子写代码？别让他们受罪了。",
        "url": "https://reddit.com/r/artificial/example_en_no_code",
    },
    {
        "id": 23,
        "source": "reddit",
        "region": "EN",
        "author_type": "kol",
        "topic": "kids_learn",
        "stance": "humanities_critical",
        "posted_at": "2026-03-22",
        "original_text": "The scarce skill in 2030 won't be coding — it'll be asking the right questions and owning the consequences. Raise kids who can do that.",
        "translation": "2030 年稀缺的不是编程，而是会提对问题、敢承担后果。把孩子培养成这样的人。",
        "url": "https://x.com/example_en_kol_humanities",
    },
    {
        "id": 24,
        "source": "oecd",
        "region": "EN",
        "author_type": "kol",
        "topic": "kids_learn",
        "stance": "ai_literacy",
        "posted_at": "2026-02-01",
        "original_text": "Future-ready curricula should combine computational thinking with AI literacy and socio-emotional skills.",
        "translation": "面向未来的课程应结合计算思维、AI 素养和社会情感能力。",
        "url": "https://oecd.org/education/example_ai_literacy_report",
    },
    {
        "id": 25,
        "source": "zhihu",
        "region": "CN",
        "author_type": "tech",
        "topic": "kids_learn",
        "stance": "still_code",
        "posted_at": "2025-10-15",
        "original_text": "让孩子学编程不是为了写代码，是为了学分解问题。AI 时代这个能力更重要。Python 还是要学。",
        "translation": "Teaching kids coding isn't about writing code but learning decomposition. This matters more in the AI era. Python still needs to be learned.",
        "url": "https://zhihu.com/answer/example_cn_still_code",
    },
    {
        "id": 26,
        "source": "xiaohongshu",
        "region": "CN",
        "author_type": "parent",
        "topic": "kids_learn",
        "stance": "still_code",
        "posted_at": "2025-11-12",
        "original_text": "朋友说 AI 来了编程没用，但我家坚持每周 Scratch 一小时。逻辑思维这东西别的课替代不了。",
        "translation": "My friend said coding is useless once AI came, but we still do Scratch one hour a week. Nothing else replaces logical thinking.",
        "url": "https://xiaohongshu.com/discovery/example_cn_still_code",
    },
    {
        "id": 27,
        "source": "weibo",
        "region": "CN",
        "author_type": "kol",
        "topic": "kids_learn",
        "stance": "humanities_critical",
        "posted_at": "2025-12-18",
        "original_text": "AI 时代最稀缺的是提问能力、审美和同理心，这些都需要阅读和讨论来培养，不是刷编程题。",
        "translation": "The scarcest skills in the AI era are asking questions, taste, and empathy — these come from reading and discussion, not coding drills.",
        "url": "https://weibo.com/example_cn_kol_humanities",
    },
    {
        "id": 28,
        "source": "bilibili",
        "region": "CN",
        "author_type": "tech",
        "topic": "kids_learn",
        "stance": "ai_literacy",
        "posted_at": "2026-01-05",
        "original_text": "我在大厂带 AI 团队，我女儿的「编程课」现在是和 AI 一起做小游戏。教语法没意义，教她怎么用 AI + 验证结果才有用。",
        "translation": "I lead an AI team at a big tech firm. My daughter's 'coding class' is now building games with AI. Teaching syntax is pointless; teaching her to use AI and verify results matters.",
        "url": "https://bilibili.com/video/example_cn_ai_literacy",
    },
    {
        "id": 29,
        "source": "wechat",
        "region": "CN",
        "author_type": "kol",
        "topic": "kids_learn",
        "stance": "ai_literacy",
        "posted_at": "2026-02-12",
        "original_text": "家长问我还要不要给孩子报编程班。我的建议：把一半时间换成 AI 素养课——prompt、事实核查、伦理判断。",
        "translation": "Parents ask if kids should still take coding classes. My advice: swap half the time for AI literacy — prompting, fact-checking, ethical judgment.",
        "url": "https://mp.weixin.qq.com/s/example_cn_kol_literacy",
    },
    {
        "id": 30,
        "source": "zhihu",
        "region": "CN",
        "author_type": "parent",
        "topic": "kids_learn",
        "stance": "fundamentals_math",
        "posted_at": "2026-02-25",
        "original_text": "我是理工妈，坚决认为数学物理比编程更底层。AI 工具每年换一套，数学一辈子不换。",
        "translation": "I'm a STEM mom. Math and physics are more fundamental than coding. AI tools change yearly; math is for life.",
        "url": "https://zhihu.com/answer/example_cn_math",
    },
    {
        "id": 31,
        "source": "xiaohongshu",
        "region": "CN",
        "author_type": "parent",
        "topic": "kids_learn",
        "stance": "humanities_critical",
        "posted_at": "2026-03-10",
        "original_text": "我家今年把编程课停了，换成了阅读俱乐部和辩论。原因很简单：代码 AI 写得比孩子好，但提问和思辨它不会。",
        "translation": "We stopped the coding class this year and switched to a book club and debate. Reason: AI writes code better than kids, but it can't ask questions or think critically.",
        "url": "https://xiaohongshu.com/discovery/example_cn_humanities",
    },
    {
        "id": 32,
        "source": "douyin",
        "region": "CN",
        "author_type": "general",
        "topic": "kids_learn",
        "stance": "no_code_needed",
        "posted_at": "2026-03-18",
        "original_text": "现在写代码 AI 一句话就搞定，还让孩子学啥编程？学点赚钱的实际技能不香吗。",
        "translation": "AI writes code in one sentence now. Why make kids learn coding? Learn something practical that makes money.",
        "url": "https://douyin.com/video/example_cn_no_code",
    },
    {
        "id": 33,
        "source": "wechat",
        "region": "CN",
        "author_type": "kol",
        "topic": "kids_learn",
        "stance": "ai_literacy",
        "posted_at": "2026-04-02",
        "original_text": "新一年趋势很清楚：从「学编程」转向「学与 AI 协作」。重点不是写代码，是会评估 AI 输出。",
        "translation": "The trend this year is clear: from 'learn to code' to 'learn to collaborate with AI'. The point isn't writing code — it's evaluating AI output.",
        "url": "https://mp.weixin.qq.com/s/example_cn_trend_2026",
    },
    {
        "id": 34,
        "source": "moe_cn",
        "region": "CN",
        "author_type": "kol",
        "topic": "kids_learn",
        "stance": "ai_literacy",
        "posted_at": "2026-01-30",
        "original_text": "推进中小学人工智能教育，构建面向未来的人机协作素养课程体系。",
        "translation": "Promote AI education in primary/secondary schools; build a future-facing human-AI collaboration curriculum.",
        "url": "http://moe.gov.cn/example_policy",
    },
    {
        "id": 35,
        "source": "commonsense",
        "region": "EN",
        "author_type": "kol",
        "topic": "kids_learn",
        "stance": "humanities_critical",
        "posted_at": "2026-01-14",
        "original_text": "Parents should prioritize media literacy and critical evaluation of AI output over tool-specific skills.",
        "translation": "家长应把媒介素养和 AI 输出的批判性评估放在工具技能之前。",
        "url": "https://commonsensemedia.org/example_ai_guide",
    },
]


def yyyymm_from_index(start_year: int, start_month: int, offset: int):
    m0 = (start_year * 12 + (start_month - 1)) + offset
    y = m0 // 12
    m = (m0 % 12) + 1
    return y, m


def generate(count: int = 500):
    out = []
    month_span = 24
    for i in range(count):
        base = BASE_POSTS[i % len(BASE_POSTS)]
        y, m = yyyymm_from_index(2024, 5, i % month_span)
        day = 1 + ((i * 7) % 28)
        posted_at = f"{y:04d}-{m:02d}-{day:02d}"
        p = dict(base)
        p["id"] = i + 1
        p["posted_at"] = posted_at
        p["url"] = f'{base["url"]}?v={i+1}'
        if base["region"] == "CN":
            p["original_text"] = f'{base["original_text"]}（样本#{i+1}）'
            if base.get("translation"):
                p["translation"] = f'{base["translation"]} (sample #{i+1})'
        else:
            p["original_text"] = f'{base["original_text"]} [sample #{i+1}]'
            if base.get("translation"):
                p["translation"] = f'{base["translation"]}（样本#{i+1}）'
        p["human_verified"] = 0
        p["human_notes"] = ""
        ai_labels = {
            "topic": p["topic"],
            "stance": p["stance"],
            "author_type": p["author_type"],
            "region": p["region"],
        }
        p["ai_confidence"] = 0.8
        p["ai_labels_json"] = json.dumps(ai_labels, ensure_ascii=False)
        out.append(p)
    return out


def month_range(start_ym: str, end_ym: str):
    sy, sm = start_ym.split("-")
    ey, em = end_ym.split("-")
    sy, sm, ey, em = int(sy), int(sm), int(ey), int(em)
    out = []
    cur = sy * 12 + (sm - 1)
    end = ey * 12 + (em - 1)
    while cur <= end:
        y = cur // 12
        m = (cur % 12) + 1
        out.append((y, m))
        cur += 1
    return out


def allocate_counts(total: int, weights):
    wsum = sum(weights) or 1
    raw = [total * w / wsum for w in weights]
    base = [int(x) for x in raw]
    remain = total - sum(base)
    frac = sorted(
        [(i, raw[i] - base[i]) for i in range(len(weights))],
        key=lambda t: t[1],
        reverse=True,
    )
    for i in range(remain):
        base[frac[i % len(frac)][0]] += 1
    return base


class PRNG:
    def __init__(self, seed: int):
        self._s = seed & 0x7FFFFFFF

    def rand(self) -> float:
        self._s = (1103515245 * self._s + 12345) & 0x7FFFFFFF
        return self._s / 2147483648.0

    def randint(self, a: int, b: int) -> int:
        if b < a:
            a, b = b, a
        return a + int(self.rand() * ((b - a) + 1))

    def choice(self, arr):
        return arr[self.randint(0, len(arr) - 1)]


def pick_weighted(rng: PRNG, items, weights):
    total = sum(weights) or 1.0
    x = rng.rand() * total
    acc = 0.0
    for it, w in zip(items, weights):
        acc += w
        if x <= acc:
            return it
    return items[-1]


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def make_url(source: str, gid: int, topic: str, stance: str):
    if source == "reddit":
        return f"https://reddit.com/r/{'Parenting' if topic=='anxiety' else 'education'}/comments/{100000 + gid}/{topic}_{stance}/"
    if source == "mumsnet":
        return f"https://mumsnet.com/talk/_/{200000 + gid}-{topic}-{stance}"
    if source == "zhihu":
        return f"https://www.zhihu.com/question/{300000 + gid}/answer/{400000 + gid}"
    if source == "xiaohongshu":
        return f"https://www.xiaohongshu.com/discovery/item/{500000 + gid}"
    if source == "weibo":
        return f"https://weibo.com/{600000 + gid}/{700000 + gid}"
    if source == "bilibili":
        return f"https://www.bilibili.com/video/BV{800000 + gid}"
    if source == "wechat":
        return f"https://mp.weixin.qq.com/s/{900000 + gid}"
    if source == "douyin":
        return f"https://www.douyin.com/video/{1000000 + gid}"
    if source == "oecd":
        return f"https://oecd.org/education/{1100000 + gid}"
    if source == "commonsense":
        return f"https://commonsensemedia.org/ai/{1200000 + gid}"
    if source == "moe_cn":
        return f"http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/{1300000 + gid}.html"
    return f"https://example.com/{gid}"


def make_text_cn(topic: str, stance: str, author_type: str, rng: PRNG):
    ctx = rng.choice(["最近刷到一堆讨论", "身边同事都在聊", "群里又吵起来了", "家长群炸了", "看完一圈我更困惑了"])
    if topic == "anxiety":
        if stance == "anxious":
            core = rng.choice([
                "感觉未来工作岗位变化太快，孩子现在学的可能几年后就不值钱了。",
                "越看越焦虑，总觉得要被时代甩下。",
                "AI 更新太快了，真的不知道该怎么给孩子规划。",
                "孩子说“反正 AI 都会了”，我一时不知道怎么接话。",
            ])
        elif stance == "balanced":
            core = rng.choice([
                "焦虑可以理解，但更重要的是让孩子会提问、会判断、会协作。",
                "与其担心被替代，不如把 AI 当工具，练信息甄别和表达。",
                "短期会乱，但长期看会出现新岗位；现在先把基础打牢。",
                "先把学习习惯和思维方式稳住，比追热点课更重要。",
            ])
        elif stance == "optimistic":
            core = rng.choice([
                "每次技术浪潮都有人焦虑，但最后都是会用工具的人跑得更快。",
                "孩子用 AI 反而学得更快，我觉得是机会不是威胁。",
                "把 AI 用起来，反而能把时间省出来做更有价值的事。",
                "别恐慌，教会孩子验证结果和承担后果就行。",
            ])
        else:
            core = rng.choice([
                "现在这些“智能体”离真正可靠还差得远，别被营销带节奏。",
                "很多人把 AI 当万能，其实场景一复杂就翻车。",
                "我看是焦虑营销，普通人先把手头事做好。",
                "等落地再说吧，现在讨论太多噪音。",
            ])
        suffix = rng.choice(["", "大家怎么看？", "有没有实操建议？", "求推荐靠谱的学习路径。", "欢迎理性讨论。"])
        return f"{ctx}：{core}{suffix}"

    if stance == "still_code":
        core = rng.choice([
            "学编程不是为了以后当码农，是为了学拆解问题和调试思维。",
            "就算 AI 写代码，懂基本原理的人更能指出哪里不对。",
            "孩子写一点点代码，才能知道 AI 输出有没有在胡编。",
            "我家坚持每周做点小项目，比刷题有效。",
        ])
    elif stance == "ai_literacy":
        core = rng.choice([
            "更应该学 AI 素养：怎么提问、怎么核查、怎么评估风险。",
            "让孩子学会用 AI 做作品，同时练“验证结果”的习惯。",
            "工具会变，但方法论不变：信息鉴别、结构化表达、伦理边界。",
            "与其教语法，不如教如何与 AI 协作完成任务。",
        ])
    elif stance == "humanities_critical":
        core = rng.choice([
            "AI 时代稀缺的是审美、同理心和批判性思维，阅读讨论更重要。",
            "写作和表达能拉开差距，别把时间都丢给编程课。",
            "会提好问题、会讲清楚观点，比会写几行代码更关键。",
            "我更愿意让孩子去辩论/写作训练，长期收益更大。",
        ])
    elif stance == "fundamentals_math":
        core = rng.choice([
            "数学统计才是底层能力，AI 工具每年换，数学不会过时。",
            "把概率和逻辑打牢，才能真正理解模型输出的可靠性。",
            "先把数理基础练好，再学工具上手会更快。",
            "理工底子强的人，用 AI 只会更强。",
        ])
    else:
        core = rng.choice([
            "AI 一句话就能生成代码，没必要再让孩子死记语法了。",
            "未来可能更像“产品表达”，描述清楚需求比写代码重要。",
            "我觉得不用强求编程，学点更通用的能力更划算。",
            "真要学也别太卷，先会用工具解决问题。",
        ])
    lead = rng.choice(["关于孩子学什么", "AI 时代教育怎么选", "最近在想这个问题", "被问到最多的就是这个"])
    suffix = rng.choice(["", "你们家怎么做？", "欢迎补充不同观点。", "求不踩坑建议。", "有资料/课程推荐吗？"])
    return f"{lead}：{core}{suffix}"


def make_text_en(topic: str, stance: str, author_type: str, rng: PRNG):
    opener = rng.choice(["Hot take", "Real question", "Genuine concern", "Not sure if it's just me", "Curious what others think"])
    if topic == "anxiety":
        if stance == "anxious":
            core = rng.choice([
                "I keep thinking about what jobs will be left by the time my kid is 18.",
                "The pace of change is messing with my head and I don't know how to plan.",
                "My teenager is saying school is pointless because AI will do everything.",
                "Every week there's a new model and it feels like the floor is moving.",
            ])
        elif stance == "balanced":
            core = rng.choice([
                "Anxiety is rational, but the action is to build judgment, writing, and collaboration skills.",
                "Treat AI like a tool: learn to verify, cite sources, and understand limits.",
                "Short-term disruption is real; long-term there will be new roles. Focus on fundamentals.",
                "The best hedge is adaptability: problem framing, communication, and learning fast.",
            ])
        elif stance == "optimistic":
            core = rng.choice([
                "Every tech shift caused panic; people adapted. This will be no different if we stay curious.",
                "My kid learns faster with AI when we teach verification and humility.",
                "AI is leverage. The winners will be the ones who can direct it well.",
                "Less doomscrolling, more building and learning.",
            ])
        else:
            core = rng.choice([
                "Most of this is marketing. These systems still fail on basic reliability.",
                "People talk like it's magic, but it breaks the moment you need accountability.",
                "Until it stops hallucinating, I'm not rearranging my whole life around it.",
                "The hype is ahead of real-world value for most families.",
            ])
        tail = rng.choice(["", "Anyone else?", "How are you handling this?", "Would love practical advice.", "Trying to stay sane here."])
        return f"{opener}: {core} {tail}".strip()

    if stance == "still_code":
        core = rng.choice([
            "Coding teaches decomposition and debugging. That matters even more with AI in the loop.",
            "If you can't read code, you can't tell when the model is wrong.",
            "I want my kid to build small projects so they learn iteration and testing.",
            "AI makes coding more accessible, not obsolete.",
        ])
    elif stance == "ai_literacy":
        core = rng.choice([
            "Teach prompting, verification, and AI ethics — tool use plus critical thinking.",
            "Kids should learn to collaborate with AI: set goals, evaluate outputs, and revise.",
            "The key skill is problem framing and validation, not memorizing syntax.",
            "AI literacy is the new media literacy.",
        ])
    elif stance == "humanities_critical":
        core = rng.choice([
            "Writing, argumentation, and taste will outlast any framework or language.",
            "Critical thinking and empathy are harder to automate — prioritize reading and discussion.",
            "The scarce skill is asking the right questions and owning consequences.",
            "Debate club did more for my kid than another coding worksheet.",
        ])
    elif stance == "fundamentals_math":
        core = rng.choice([
            "Math and stats are the moat. If you understand uncertainty, AI is a tool not a black box.",
            "Foundations beat fads. Probability and linear algebra will keep paying off.",
            "A strong quantitative base makes learning new tools trivial.",
            "Teach fundamentals first, then tools.",
        ])
    else:
        core = rng.choice([
            "If you can describe what you want, AI can generate the code. Why force syntax early?",
            "Maybe we should focus on product thinking and communication rather than coding drills.",
            "Tooling is changing too fast for language-specific classes to age well.",
            "I’d rather teach kids to build with tools than struggle with boilerplate.",
        ])
    end = rng.choice(["", "Thoughts?", "What are you doing with your kids?", "Open to counterarguments.", "Would love resources."])
    return f"{opener}: {core} {end}".strip()


def cn_translation_stub(topic: str, stance: str, rng: PRNG):
    if topic == "anxiety":
        return rng.choice([
            "我有点担心未来的工作会怎么变，孩子该怎么准备。",
            "变化太快了，规划变得很难。",
            "孩子说学习没意义，我不知道怎么回应。",
            "想听听大家有没有更理性的应对方法。",
        ])
    return rng.choice([
        "AI 时代孩子到底该学什么？我更倾向于培养通用能力。",
        "感觉重点是会用工具并能验证输出，而不是死记语法。",
        "大家的选择不同，但希望少点焦虑多点实践。",
        "欢迎分享你们的做法。",
    ])


def en_translation_stub(topic: str, stance: str, rng: PRNG):
    if topic == "anxiety":
        return rng.choice([
            "I’m anxious about how fast jobs are changing and how to prepare kids.",
            "The pace is overwhelming and planning feels impossible.",
            "My kid says school is pointless because of AI; I’m not sure what to say.",
            "Trying to stay practical and not panic.",
        ])
    return rng.choice([
        "What should kids learn in the AI era? I lean toward transferable skills.",
        "The point is using tools and verifying outputs, not memorizing syntax.",
        "Different paths work, but practice matters more than hype.",
        "Would love to hear what others are doing.",
    ])


def generate_focused(
    count: int,
    start_ym: str = "2025-10",
    end_ym: str = "2026-04",
    weights=None,
):
    weights = weights or [3, 4, 5, 7, 9, 12, 16]
    months = month_range(start_ym, end_ym)
    if len(weights) != len(months):
        raise ValueError("weights length must match month span")
    per_month = allocate_counts(count, weights)

    out = []
    gid = 0
    for mi, (y, m) in enumerate(months):
        for j in range(per_month[mi]):
            base = BASE_POSTS[gid % len(BASE_POSTS)]
            day = 1 + (((gid * 7) + (j * 3)) % 28)
            posted_at = f"{y:04d}-{m:02d}-{day:02d}"
            p = dict(base)
            p["id"] = gid + 1
            p["posted_at"] = posted_at
            p["url"] = f'{base["url"]}?v={gid+1}'
            if base["region"] == "CN":
                p["original_text"] = f'{base["original_text"]}（样本#{gid+1}）'
                if base.get("translation"):
                    p["translation"] = f'{base["translation"]} (sample #{gid+1})'
            else:
                p["original_text"] = f'{base["original_text"]} [sample #{gid+1}]'
                if base.get("translation"):
                    p["translation"] = f'{base["translation"]}（样本#{gid+1}）'
            p["human_verified"] = 0
            p["human_notes"] = ""
            ai_labels = {
                "topic": p["topic"],
                "stance": p["stance"],
                "author_type": p["author_type"],
                "region": p["region"],
            }
            p["ai_confidence"] = 0.8
            p["ai_labels_json"] = json.dumps(ai_labels, ensure_ascii=False)
            out.append(p)
            gid += 1
    return out


def generate_focused_realistic(
    count: int,
    start_ym: str = "2025-10",
    end_ym: str = "2026-04",
    weights=None,
    base_seed: int = 20261004,
):
    weights = weights or [3, 4, 5, 7, 9, 12, 16]
    months = month_range(start_ym, end_ym)
    if len(weights) != len(months):
        raise ValueError("weights length must match month span")
    per_month = allocate_counts(count, weights)

    topic_kids_p = [0.46, 0.48, 0.50, 0.53, 0.56, 0.60, 0.62]
    region_cn_p = [0.36, 0.38, 0.42, 0.48, 0.55, 0.60, 0.63]

    sources_en = ["reddit", "mumsnet", "x", "oecd", "commonsense"]
    sources_en_w = [0.58, 0.14, 0.16, 0.06, 0.06]
    sources_cn = ["zhihu", "xiaohongshu", "weibo", "bilibili", "wechat", "douyin", "moe_cn"]
    sources_cn_w = [0.24, 0.20, 0.18, 0.12, 0.16, 0.08, 0.02]

    author_types = ["parent", "tech", "general", "kol"]
    author_w = [0.34, 0.26, 0.24, 0.16]

    anxiety_stances = ["anxious", "balanced", "optimistic", "dismissive"]
    anxiety_w_by_m = [
        [0.56, 0.24, 0.14, 0.06],
        [0.54, 0.26, 0.15, 0.05],
        [0.50, 0.29, 0.16, 0.05],
        [0.46, 0.32, 0.17, 0.05],
        [0.42, 0.34, 0.18, 0.06],
        [0.38, 0.36, 0.20, 0.06],
        [0.34, 0.38, 0.22, 0.06],
    ]
    kids_stances = ["still_code", "ai_literacy", "humanities_critical", "fundamentals_math", "no_code_needed"]
    kids_w_by_m = [
        [0.38, 0.22, 0.18, 0.16, 0.06],
        [0.35, 0.25, 0.18, 0.16, 0.06],
        [0.32, 0.28, 0.18, 0.15, 0.07],
        [0.28, 0.32, 0.18, 0.15, 0.07],
        [0.25, 0.35, 0.17, 0.15, 0.08],
        [0.22, 0.38, 0.17, 0.14, 0.09],
        [0.20, 0.40, 0.17, 0.13, 0.10],
    ]

    out = []
    gid = 0
    for mi, (y, m) in enumerate(months):
        for _ in range(per_month[mi]):
            rng = PRNG(base_seed + gid * 97 + mi * 131)
            topic = "kids_learn" if rng.rand() < topic_kids_p[mi] else "anxiety"
            region = "CN" if rng.rand() < region_cn_p[mi] else "EN"

            if region == "CN":
                source = pick_weighted(rng, sources_cn, sources_cn_w)
            else:
                source = pick_weighted(rng, sources_en, sources_en_w)

            if source in ("oecd", "commonsense", "moe_cn"):
                author_type = "kol"
            elif source == "x":
                author_type = pick_weighted(rng, author_types, [0.18, 0.32, 0.20, 0.30])
            elif source == "wechat":
                author_type = pick_weighted(rng, author_types, [0.18, 0.30, 0.12, 0.40])
            else:
                author_type = pick_weighted(rng, author_types, author_w)

            if topic == "anxiety":
                weights_st = list(anxiety_w_by_m[mi])
                if author_type == "parent":
                    weights_st[0] += 0.06
                    weights_st[1] -= 0.03
                    weights_st[2] -= 0.02
                if author_type == "tech":
                    weights_st[1] += 0.05
                    weights_st[0] -= 0.03
                if author_type == "kol":
                    weights_st[2] += 0.04
                    weights_st[0] -= 0.02
                stance = pick_weighted(rng, anxiety_stances, [max(0.01, w) for w in weights_st])
            else:
                weights_st = list(kids_w_by_m[mi])
                if author_type == "tech":
                    weights_st[0] += 0.05
                    weights_st[1] += 0.04
                    weights_st[4] -= 0.03
                if author_type == "parent":
                    weights_st[3] += 0.03
                    weights_st[4] += 0.02
                if author_type == "kol":
                    weights_st[1] += 0.05
                    weights_st[2] += 0.03
                stance = pick_weighted(rng, kids_stances, [max(0.01, w) for w in weights_st])

            day = 1 + rng.randint(0, 27)
            posted_at = f"{y:04d}-{m:02d}-{day:02d}"
            url = make_url(source, gid, topic, stance)

            if region == "CN":
                original_text = make_text_cn(topic, stance, author_type, rng)
                translation = None if rng.rand() < 0.28 else en_translation_stub(topic, stance, rng)
            else:
                original_text = make_text_en(topic, stance, author_type, rng)
                translation = None if rng.rand() < 0.25 else cn_translation_stub(topic, stance, rng)

            verified = 1 if rng.rand() < 0.08 else 0
            ai_topic = topic
            ai_stance = stance
            ai_author = author_type
            ai_region = region

            override = False
            if verified and rng.rand() < 0.18:
                override = True
                if topic == "anxiety":
                    ai_stance = pick_weighted(rng, anxiety_stances, [1, 1, 1, 1])
                else:
                    ai_stance = pick_weighted(rng, kids_stances, [1, 1, 1, 1, 1])
                if ai_stance == stance:
                    ai_stance = anxiety_stances[(anxiety_stances.index(stance) + 1) % len(anxiety_stances)] if topic == "anxiety" else kids_stances[(kids_stances.index(stance) + 1) % len(kids_stances)]

            conf_base = 0.62 + 0.30 * rng.rand()
            if override:
                conf_base -= 0.18
            if source in ("oecd", "moe_cn"):
                conf_base += 0.08
            if author_type == "general":
                conf_base -= 0.04
            ai_confidence = round(clamp(conf_base, 0.50, 0.98), 2)

            human_notes = ""
            if verified:
                if override:
                    human_notes = rng.choice([
                        "人工复核：立场与AI判断不一致，已调整为更贴近原文语气。",
                        "复核后发现AI过度乐观/悲观，已按原文修正。",
                        "标注纠错：AI stance 误判，已修正。",
                    ])
                else:
                    human_notes = rng.choice(["", "人工复核通过。", "抽检通过。", "已确认无误。"])

            ai_labels = {
                "topic": ai_topic,
                "stance": ai_stance,
                "author_type": ai_author,
                "region": ai_region,
            }
            out.append(
                {
                    "id": gid + 1,
                    "source": source,
                    "region": region,
                    "author_type": author_type,
                    "topic": topic,
                    "stance": stance,
                    "original_text": original_text,
                    "translation": translation,
                    "url": url,
                    "posted_at": posted_at,
                    "ai_confidence": ai_confidence,
                    "ai_labels_json": json.dumps(ai_labels, ensure_ascii=False, separators=(",", ":")),
                    "human_verified": verified,
                    "human_notes": human_notes,
                }
            )
            gid += 1
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=500)
    ap.add_argument("--mode", choices=["spread", "focus", "focus_real"], default="spread")
    ap.add_argument("--start", default="2025-10")
    ap.add_argument("--end", default="2026-04")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    if args.mode == "focus_real":
        data = generate_focused_realistic(args.count, start_ym=args.start, end_ym=args.end)
    elif args.mode == "focus":
        data = generate_focused(args.count, start_ym=args.start, end_ym=args.end)
    else:
        data = generate(args.count)

    s = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(s)
    else:
        print(s)
