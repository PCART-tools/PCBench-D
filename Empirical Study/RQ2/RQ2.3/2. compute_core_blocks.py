#!/usr/bin/env python3
"""
Compute core_blocks for all block_analysis.json files.

Rules (classification delta from delta_vi1_to_vi[algo]["delta"]):
  - delta != 0: select block(s) with delta_vi_to_restored in the opposite
    direction (positive delta → most negative delta_vi_to_restored,
    negative delta → most positive delta_vi_to_restored), but only if the
    extreme actually restores toward the original rank:
      * delta > 0 (rank decreased, e.g. 5->1): require the most negative
        delta_vi_to_restored < 0, otherwise no core_block
      * delta < 0 (rank increased, e.g. 1->5): require the most positive
        delta_vi_to_restored > 0, otherwise no core_block
  - delta == 0: only blocks with delta_vi_to_restored == 0

Input:  block_analysis.json (must have "delta_vi1_to_vi", "blocks", "algorithms")
Output: same file, with "core_blocks" field added.
"""

import json, os, sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
KV_DIR = SCRIPT_DIR.parent


BASE_DIR = KV_DIR / "RQ2.2" / "cases_split"

def select_core_blocks_nonzero(delta: int, blocks: list) -> list[str]:
    """Select core_blocks for delta != 0: pick the opposite extreme.

    delta > 0 → most negative delta_vi_to_restored (must be < 0 to count)
    delta < 0 → most positive delta_vi_to_restored (must be > 0 to count)

    If the extreme does not actually restore toward the original rank,
    return [] (no core_block).
    """
    if not blocks:
        return []

    if delta > 0:
        best_val = min(b["delta_vi_to_restored"] for b in blocks)
        if best_val >= 0:
            return []
        return [b["block"] for b in blocks if b["delta_vi_to_restored"] == best_val]
    else:
        best_val = max(b["delta_vi_to_restored"] for b in blocks)
        if best_val <= 0:
            return []
        return [b["block"] for b in blocks if b["delta_vi_to_restored"] == best_val]


def select_core_blocks_delta0(blocks: list) -> list[str]:
    """Select core_blocks for delta == 0: only blocks with delta_vi_to_restored == 0."""
    if not blocks:
        return []

    return [b["block"] for b in blocks if b["delta_vi_to_restored"] == 0]


def read_comment_blocks(diff_dir: Path) -> set[str]:
    """读取 diff_dir/comment.txt，返回不参与 core_block 判定的 block 名集合。

    每行一个 block 名（如 block_001），忽略空行与 # 注释。
    文件不存在时返回空集合。
    """
    p = diff_dir / "comment.txt"
    if not p.is_file():
        return set()
    exclude: set[str] = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        exclude.add(s)
    return exclude


def process_json(json_path: Path, dry_run: bool = True) -> dict | None:
    """Process a single block_analysis.json."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("error") is not None:
        return None

    algorithms = data.get("algorithms", [])
    blocks = data.get("blocks", [])
    delta_vi1_to_vi = data.get("delta_vi1_to_vi", {})

    if not algorithms or not delta_vi1_to_vi or not blocks:
        return None

    core_blocks = data.get("core_blocks", {})
    added_algorithms = {}
    exclude = read_comment_blocks(json_path.parent)

    for algo in algorithms:
        dvi_info = delta_vi1_to_vi.get(algo)
        if dvi_info is None:
            continue

        classification_delta = dvi_info["delta"]
        if classification_delta is None:
            continue

        algo_blocks = []
        for b in blocks:
            if b["block"] in exclude:
                continue
            if not b.get("patch_ok", True):
                continue
            algo_data = b.get("algorithms", {}).get(algo)
            if algo_data is None:
                continue
            algo_blocks.append({
                "block": b["block"],
                "delta_vi_to_restored": algo_data["delta_vi_to_restored"],
            })

        if not algo_blocks:
            continue

        if classification_delta == 0:
            selected = select_core_blocks_delta0(algo_blocks)
        else:
            selected = select_core_blocks_nonzero(classification_delta, algo_blocks)

        core_blocks[algo] = selected
        added_algorithms[algo] = selected

    if not added_algorithms:
        return None

    data["core_blocks"] = core_blocks
    if not dry_run:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    return {
        "case": data["case"],
        "added_algorithms": added_algorithms,
    }


def main():
    dry_run = "--apply" not in sys.argv
    if dry_run:
        print("=" * 60)
        print("DRY-RUN mode (preview only)")
        print("Use --apply to actually write files")
        print("=" * 60)
    else:
        print("=" * 60)
        print("APPLY mode")
        print("=" * 60)

    total_jsons = 0
    modified_count = 0

    for root, dirs, files in os.walk(BASE_DIR, followlinks=True):
        for fname in files:
            if fname != "block_analysis.json":
                continue
            json_path = Path(root) / fname
            total_jsons += 1

            result = process_json(json_path, dry_run=dry_run)
            if result is None:
                continue

            modified_count += 1
            case = result["case"]
            added = result["added_algorithms"]
            algo_summary = ", ".join(
                f"{algo}=[{','.join(blocks)}]" for algo, blocks in added.items()
            )
            print(f"[MOD] {case}: {algo_summary}")

    print()
    print(f"Scanned {total_jsons} JSONs, modified {modified_count}")

    if dry_run:
        print("DRY-RUN only — use --apply to write changes.")


if __name__ == "__main__":
    main()
