#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add block_sign_labels to all block_analysis.json files.

For each core_block, generate a label based on delta_vi_to_restored signs:
  - pos (delta > 0)  → down
  - neg (delta < 0)  → up
  - zero (delta = 0) → flat

Label format:
  - class:          map_{sign}_token_{sign}
  - function/method: map_{sign}_token_{sign}_tree_{sign}
"""

import json, os
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
KV_DIR = SCRIPT_DIR.parent


SPLIT_DIR = KV_DIR / "RQ2.2" / "cases_split"

ALGO_PREFIXES = ["map", "token", "tree"]


def delta_to_sign(delta: int) -> str:
    """Map delta value to sign string.

    Args:
        delta: integer value of delta_vi_to_restored

    Returns:
        "down" (>0), "up" (<0), or "flat" (=0)
    """
    if delta > 0:
        return "down"
    elif delta < 0:
        return "up"
    else:
        return "flat"


def build_sign_label(delta_map: dict[str, int], algo_keys: list[str]) -> str:
    """Build sign label from per-algorithm deltas.

    Args:
        delta_map: {"mapBased": 5, "tokenBased": -3, ...}
        algo_keys: ["mapBased", "tokenBased"] or ["mapBased", "tokenBased", "treeBased"]

    Returns:
        e.g. "map_down_token_up" or "map_down_token_up_tree_flat"
    """
    prefix_map = {
        "mapBased": "map",
        "tokenBased": "token",
        "treeBased": "tree",
    }
    parts = []
    for key in algo_keys:
        short = prefix_map.get(key, key)
        sign = delta_to_sign(delta_map.get(key, 0))
        parts.append(f"{short}_{sign}")
    return "_".join(parts)


def find_all_jsons() -> dict[str, list[Path]]:
    """Find all block_analysis.json files under cases_split/, grouped by type.

    Returns:
        {"class": [...], "function": [...], "method": [...]}
    """
    by_type: dict[str, list[Path]] = defaultdict(list)

    for root, dirs, files in os.walk(SPLIT_DIR, followlinks=True):
        for fname in files:
            if fname == "block_analysis.json":
                full_path = Path(root) / fname
                rel = full_path.relative_to(SPLIT_DIR)
                parts = rel.parts
                if len(parts) >= 4:
                    case_type = parts[3]  # class / function / method
                    if case_type in ("class", "function", "method"):
                        by_type[case_type].append(full_path)

    return dict(by_type)


def label_one_json(json_path: Path) -> str | None:
    """Label core_blocks in a single block_analysis.json and write back.

    Args:
        json_path: absolute path to block_analysis.json

    Returns:
        None on success, error string on failure.
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return f"read failed: {e}"

    path_str = str(json_path)
    if "/class/" in path_str:
        algo_keys = ["mapBased", "tokenBased"]
    elif "/function/" in path_str or "/method/" in path_str:
        algo_keys = ["mapBased", "tokenBased", "treeBased"]
    else:
        algo_keys = data.get("algorithms", [])
        if not algo_keys:
            return "cannot determine algorithm set from path"

    blocks = data.get("blocks", [])
    core_blocks = data.get("core_blocks", {})

    block_index: dict[str, dict] = {}
    for b in blocks:
        block_index[b["block"]] = b

    label_groups: dict[str, list[str]] = defaultdict(list)
    seen: set[str] = set()

    for algo_name, block_ids in core_blocks.items():
        for block_id in block_ids:
            if block_id in seen:
                continue
            seen.add(block_id)

            if block_id not in block_index:
                continue

            block_entry = block_index[block_id]
            algos = block_entry.get("algorithms", {})

            delta_map: dict[str, int] = {}
            for key in algo_keys:
                algo_data = algos.get(key, {})
                delta_map[key] = algo_data.get("delta_vi_to_restored", 0)

            label = build_sign_label(delta_map, algo_keys)
            label_groups[label].append(block_id)

    data["block_sign_labels"] = dict(label_groups)

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        return f"write failed: {e}"

    return None


def main():
    all_jsons = find_all_jsons()
    total = sum(len(v) for v in all_jsons.values())
    print(f"Found {total} block_analysis.json files")
    for ct in ("class", "function", "method"):
        count = len(all_jsons.get(ct, []))
        print(f"  {ct}: {count}")

    success = 0
    failed: list[tuple[str, str]] = []

    for case_type in ("class", "function", "method"):
        paths = all_jsons.get(case_type, [])
        print(f"\n[{case_type}] processing {len(paths)}...")
        for path in sorted(paths):
            try:
                rel = path.relative_to(SPLIT_DIR)
            except ValueError:
                rel = path
            err = label_one_json(path)
            if err is None:
                success += 1
            else:
                failed.append((str(rel), err))
                print(f"  [FAIL] {rel}: {err}")

    print(f"\nDone: {success} success, {len(failed)} failed")
    if failed:
        for rel, err in failed:
            print(f"  {rel}: {err}")


if __name__ == "__main__":
    main()
