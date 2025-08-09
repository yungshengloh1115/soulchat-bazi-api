from datetime import datetime
from typing import Dict, Any, Tuple

# Very small helper lookups (placeholders!)
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
EARTHLY_BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
FIVE_ELEMENTS = ["木","火","土","金","水"]

STEM_TO_ELEMENT = {
    "甲":"木","乙":"木","丙":"火","丁":"火","戊":"土",
    "己":"土","庚":"金","辛":"金","壬":"水","癸":"水",
}

BRANCH_TO_ELEMENT = {
    "子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火",
    "午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水",
}

# WARNING: This is NOT a real BaZi engine. It creates deterministic demo output
# so your app can integrate end-to-end. Swap with a true library/service later.

def cyc_index(n: int, base: int) -> int:
    return n % base

def pillar_from_index(i: int) -> Tuple[str, str]:
    stem = HEAVENLY_STEMS[cyc_index(i, 10)]
    branch = EARTHLY_BRANCHES[cyc_index(i, 12)]
    return stem, branch

def compute_bazi(birth_dt: datetime, use_true_solar_time: bool=False):
    # Deterministic but fake mapping based on date parts
    y = birth_dt.year
    m = birth_dt.month
    d = birth_dt.day
    h = birth_dt.hour

    year_idx = (y - 4)  # 4 CE as 甲子 anchor (placeholder)
    month_idx = (y * 12 + m)
    day_idx = (y * 372 + m * 31 + d)
    hour_idx = (day_idx * 24 + h)

    y_p = pillar_from_index(year_idx)
    m_p = pillar_from_index(month_idx)
    d_p = pillar_from_index(day_idx)
    h_p = pillar_from_index(hour_idx)

    pillars = {
        "year": {"stem": y_p[0], "branch": y_p[1]},
        "month": {"stem": m_p[0], "branch": m_p[1]},
        "day": {"stem": d_p[0], "branch": d_p[1]},
        "hour": {"stem": h_p[0], "branch": h_p[1]},
    }

    # Crude element tallies
    counts = {e: 0 for e in FIVE_ELEMENTS}
    for p in pillars.values():
        counts[STEM_TO_ELEMENT[p["stem"]]] += 1
        counts[BRANCH_TO_ELEMENT[p["branch"]]] += 1

    dominant = max(counts, key=lambda k: counts[k])
    balance_score = {e: round(counts[e] / 8.0, 2) for e in FIVE_ELEMENTS}

    dbg = {
        "year_idx": year_idx,
        "month_idx": month_idx,
        "day_idx": day_idx,
        "hour_idx": hour_idx,
        "raw_counts": counts,
    }

    elements = {
        "dominant": dominant,
        "balance": balance_score,
    }

    return pillars, elements, dbg

TRAIT_TEMPLATES = {
    "木": ["成长导向","重视原则","富有创造力"],
    "火": ["表达力强","热情外向","执行果断"],
    "土": ["稳重务实","可靠守信","耐心细致"],
    "金": ["逻辑清晰","重效率","目标导向"],
    "水": ["思维灵活","适应性强","善于沟通"],
}

def summarize_traits(pillars: Dict[str, Dict[str, str]], elements: Dict[str, Any]) -> Dict[str, Any]:
    dom = elements.get("dominant", "木")
    traits = TRAIT_TEMPLATES.get(dom, TRAIT_TEMPLATES["木"])
    tips = {
        "木": "设立清晰里程碑，避免无限制地扩张目标。",
        "火": "行动前列出两条备选方案，降低冲动决策风险。",
        "土": "给创新留出试错空间，避免过度保守。",
        "金": "关注团队节奏，避免只看效率忽略情绪。",
        "水": "为长期项目设置边界，防止频繁切换精力分散。",
    }
    return {
        "dominant_element": dom,
        "core_traits": traits,
        "action_tip": tips.get(dom, "保持学习与复盘，持续微调策略。"),
        "disclaimer": "演示版性格摘要。正式版请接入真实八字推算引擎。",
    }
