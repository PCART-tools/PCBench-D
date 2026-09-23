#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对 RQ2/cases/ 下所有 case 做 Rank 变化原因分析（b4 + b5）。
原因分类结果集中保存到脚本同级 output/cause_classification.json。

逻辑来源：docs/rank_transition_cause_analysis.md
"""

import json
import re
import os
from pathlib import Path

# =========================
# 1. 配置
# =========================

# cases 数据位于脚本同级目录下；如目录位置变化，请替换为实际路径
CASES_ROOT = Path(__file__).resolve().parent / "cases"
ALGORITHMS = ["mapBased", "tokenBased", "treeBased"]

CAUSE_LABELS = {
    "candidates": "candidates",
    "dep_rep": "弃用-替代",
    "combined": "共同原因",
    "special": "特殊情况",
    "undetermined": "未确定",
}


# =========================
# 2. Case 名解析
# =========================

def parse_case_name(dirname: str):
    """
    从 case 目录名 D_FQN-R_FQN-version 解析出 D_FQN 和 R_FQN。

    策略：version 可能包含 '-'（如 jax-v0.4.14、networkx-2.8.8），
    从右往左逐段尝试 version 的段数，找到使 D_FQN-R_FQN 段数为偶数
    （即 '-' 数为奇数）的分界点。
    """
    parts = dirname.split("-")
    for n_version in range(1, len(parts)):
        remaining = parts[:-n_version]
        # remaining 段数必须为偶数 → 其内部 '-' 数为奇数
        if len(remaining) >= 2 and len(remaining) % 2 == 0:
            mid = len(remaining) // 2
            d_fqn = "-".join(remaining[:mid])
            r_fqn = "-".join(remaining[mid:])
            version = "-".join(parts[-n_version:])
            return d_fqn, r_fqn, version
    # fallback: 如果上述逻辑失败（极少情况），尝试去掉最后一个 '-' 段
    for n_version in range(1, len(parts)):
        remaining = parts[:-n_version]
        if len(remaining) >= 2 and len(remaining) % 2 == 0:
            mid = len(remaining) // 2
            return "-".join(remaining[:mid]), "-".join(remaining[mid:]), "-".join(parts[-n_version:])
    raise ValueError(f"Cannot parse case name: {dirname}")


# =========================
# 3. 数据加载
# =========================

def load_json(path: Path):
    """加载 rank JSON 文件。"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_lookup(rank_list: list) -> dict:
    """将 [{api_name, score, rank}, ...] 转为 {api_name: {score, rank}}。"""
    return {item["api_name"]: {"score": item["score"], "rank": item["rank"]} for item in rank_list}


def find_version_dir(result_dir: Path, prefix: str, exclude_prefix: str = None):
    """
    在 result/ 下找匹配前缀的子目录。
    如 prefix='Vi-1' 找 Vi-1_*；prefix='Vi' + exclude_prefix='Vi-1' 找 Vi_*。
    """
    for child in sorted(result_dir.iterdir()):
        if child.is_dir() and child.name.startswith(prefix):
            if exclude_prefix and child.name.startswith(exclude_prefix):
                continue
            return child
    return None


# =========================
# 4. b4: 排名变化分析
# =========================

def classify_ratio(ratio: float) -> str:
    """ΔC / ΔS → 7 个区间之一。使用容差处理浮点数判等。"""
    eps = 1e-9
    if ratio < -1 - eps:
        return "lt_minus1"
    if abs(ratio - (-1)) <= eps:
        return "eq_minus1"
    if ratio < -eps:
        return "gt_minus1_lt_0"
    if abs(ratio) <= eps:
        return "eq_0"
    if ratio < 1 - eps:
        return "gt_0_lt_1"
    if abs(ratio - 1) <= eps:
        return "eq_1"
    return "gt_1"


def init_value_dict(direction: str = "") -> dict:
    return {
        "direction": direction,
        "deltaR": 0,
        "deltaS": 0.0,
        "rangeSize": 0,
        "notexist": 0,
        "notDec": 0,
        "deltaSZero": 0,
        "lt_minus1": 0,
        "eq_minus1": 0,
        "gt_minus1_lt_0": 0,
        "eq_0": 0,
        "gt_0_lt_1": 0,
        "eq_1": 0,
        "gt_1": 0,
    }


def analyze_rank_transition(v1_lookup: dict, v2_lookup: dict, r_fqn: str) -> dict:
    """分析 R_FQN 在 v1→v2 间的排名变化。"""
    if r_fqn not in v1_lookup or r_fqn not in v2_lookup:
        return None

    r1 = v1_lookup[r_fqn]
    r2 = v2_lookup[r_fqn]

    if r1["rank"] == r2["rank"]:
        result = init_value_dict("None")
        result["deltaR"] = 0
        result["deltaS"] = 0.0
        return result

    total = (len(v1_lookup) + len(v2_lookup)) / 2
    result = init_value_dict()

    if r1["rank"] > r2["rank"]:
        # Ascending: 排名上升 (数字变小)
        result["direction"] = "A"
        result["deltaR"] = r1["rank"] - r2["rank"]
        result["deltaS"] = r2["score"] - r1["score"]  # 不做 abs
        result["rangeSize"] = r1["rank"] - 1

        for api, info in v1_lookup.items():
            if not (1 <= info["rank"] <= r1["rank"] - 1):
                continue
            if api not in v2_lookup:
                result["notexist"] += 1
            elif v2_lookup[api]["rank"] < r2["rank"]:
                result["notDec"] += 1
            elif result["deltaS"] != 0:
                delta_c = v2_lookup[api]["score"] - info["score"]
                cat = classify_ratio(delta_c / result["deltaS"])
                result[cat] += 1
    else:
        # Descending: 排名下降 (数字变大)
        result["direction"] = "D"
        result["deltaR"] = r2["rank"] - r1["rank"]
        result["deltaS"] = r1["score"] - r2["score"]  # 不做 abs
        result["rangeSize"] = r2["rank"] - 1

        for api, info in v2_lookup.items():
            if not (1 <= info["rank"] <= r2["rank"] - 1):
                continue
            if api not in v1_lookup:
                result["notexist"] += 1
            elif v1_lookup[api]["rank"] < r1["rank"]:
                result["notDec"] += 1
            elif result["deltaS"] != 0:
                delta_c = v1_lookup[api]["score"] - info["score"]
                cat = classify_ratio(delta_c / result["deltaS"])
                result[cat] += 1

    if result["deltaS"] == 0:
        result["deltaSZero"] = 1

    return result


# =========================
# 5. b5: 原因分类
# =========================

def classify_cause(values: dict):
    """从 ValueDict 判定突变原因。返回 (cause_key, special_reason|None)。"""
    range_size = values.get("rangeSize", 0)
    not_dec = values.get("notDec", 0)
    delta_s_zero = values.get("deltaSZero", 0)
    eq_minus1 = values.get("eq_minus1", 0)
    notexist = values.get("notexist", 0)
    lt_minus1 = values.get("lt_minus1", 0)
    gt_minus1_lt_0 = values.get("gt_minus1_lt_0", 0)
    eq_0 = values.get("eq_0", 0)
    gt_0_lt_1 = values.get("gt_0_lt_1", 0)
    gt_1 = values.get("gt_1", 0)
    eq_1 = values.get("eq_1", 0)

    # 预检：特殊情况
    if range_size == not_dec:
        return ("special", "rangeSize == notDec")
    if eq_1 != 0:
        return ("special", "eq_1 != 0")

    # deltaSZero → candidates
    if delta_s_zero != 0:
        return ("candidates", None)

    # 聚合指标
    dep_rep = gt_0_lt_1 + eq_0 + gt_minus1_lt_0
    cand = gt_1 + lt_minus1 + notexist
    combined = eq_minus1

    # 判定
    if combined >= dep_rep and combined >= cand:
        return ("combined", None)
    if dep_rep == cand:
        return ("combined", None)
    if dep_rep > cand:
        return ("dep_rep", None)
    else:
        return ("candidates", None)


# =========================
# 6. 算法间一致性汇总
# =========================

def final_cause_from_algos(algo_causes: dict) -> str:
    """
    algo_causes: {"mapBased": "candidates", "tokenBased": "dep_rep", ...}
    返回最终原因。
    """
    # special 只表示该算法不适用或排名未发生变化，不参与 case 级原因汇总。
    causes = [cause for cause in algo_causes.values() if cause != "special"]
    if not causes:
        return "undetermined"

    # 全部相同（非 special）→ 该类别
    if len(set(causes)) == 1:
        return causes[0]

    # 有不同类别 → combined（算法不一致）
    return "combined"


# =========================
# 7. 单 case 处理
# =========================

def process_case(case_dir: Path) -> dict:
    """处理单个 case，返回分析结果。不写文件。"""
    dirname = case_dir.name
    result_dir = case_dir / "result"

    # 解析 case 名
    try:
        d_fqn, r_fqn, version = parse_case_name(dirname)
    except ValueError as e:
        return {"error": str(e), "case_dir": str(case_dir)}

    # 定位 Vi-1 和 Vi 目录
    vi_minus_1_dir = find_version_dir(result_dir, "Vi-1")
    vi_dir = find_version_dir(result_dir, "Vi", exclude_prefix="Vi-1")

    if not vi_minus_1_dir or not vi_dir:
        missing = []
        if not vi_minus_1_dir:
            missing.append("Vi-1")
        if not vi_dir:
            missing.append("Vi")
        return {"error": f"Missing version dirs: {missing}", "case_dir": str(case_dir)}

    # 逐算法分析
    value_dicts = {}
    algo_causes = {}

    for algo in ALGORITHMS:
        v1_file = vi_minus_1_dir / f"{algo}.json"
        v2_file = vi_dir / f"{algo}.json"

        if not v1_file.exists() or not v2_file.exists():
            continue

        try:
            v1_data = load_json(v1_file)
            v2_data = load_json(v2_file)
        except (json.JSONDecodeError, IOError):
            continue

        v1_lookup = build_lookup(v1_data)
        v2_lookup = build_lookup(v2_data)

        values = analyze_rank_transition(v1_lookup, v2_lookup, r_fqn)
        if values is None:
            # R_FQN 不在某个版本中
            continue

        cause_key, special_reason = classify_cause(values)
        value_dicts[algo] = values
        algo_causes[algo] = {
            "cause": cause_key,
            "special_reason": special_reason,
        }

    # 一致性汇总
    cause_keys = {algo: info["cause"] for algo, info in algo_causes.items()}
    final = final_cause_from_algos(cause_keys)

    return {
        "d_fqn": d_fqn,
        "r_fqn": r_fqn,
        "version": version,
        "value_dicts": value_dicts,
        "cause_classifications": algo_causes,
        "final_cause": final,
    }


# =========================
# 8. 主流程
# =========================

def discover_cases() -> list:
    """发现所有包含 result/ 子目录的 case 目录。"""
    case_dirs = []
    for root, dirs, files in os.walk(CASES_ROOT):
        if "result" in dirs:
            case_dirs.append(Path(root))
            dirs.clear()  # 不再深入
    return sorted(case_dirs)


def main():
    case_dirs = discover_cases()
    print(f"发现 {len(case_dirs)} 个 case")

    success = 0
    errors = []
    classification_results = {}
    stats = {
        "candidates": 0,
        "dep_rep": 0,
        "combined": 0,
        "special": 0,
        "undetermined": 0,
    }

    for case_dir in case_dirs:
        result = process_case(case_dir)
        if "error" in result:
            errors.append(result)
            continue

        experiment = case_dir.relative_to(CASES_ROOT).parts[0]
        classification_results[f"{experiment}-{case_dir.name}"] = {
            **result["cause_classifications"],
            "final_cause": result["final_cause"],
        }
        success += 1
        fc = result["final_cause"]
        if fc in stats:
            stats[fc] += 1

    print(f"\n成功: {success}, 失败: {len(errors)}")
    print(f"\n原因分布:")
    for k, v in stats.items():
        print(f"  {CAUSE_LABELS.get(k, k)}: {v}")

    if errors:
        print(f"\n错误详情 (前10条):")
        for err in errors[:10]:
            print(f"  {err['case_dir']}: {err['error']}")

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "cause_classification.json"
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(classification_results, f, indent=2, ensure_ascii=False)

    print(f"\n原因分类结果已保存到: {output_file}")


if __name__ == "__main__":
    main()
