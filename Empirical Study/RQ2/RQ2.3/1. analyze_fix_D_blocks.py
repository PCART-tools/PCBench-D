#!/usr/bin/env python3
"""
Analyze dep_rep/fix_D case diff blocks:
1. Read deltas and 10% threshold from analysis.md, identify threshold-meeting algorithms
2. Compute baseline rank for each algorithm (Vi-1 replacement API score ranked in Vi minus-self pool)
3. For each block, apply reverse patch → restored, rank in minus-self pool
Output: diff_analysis/block_analysis.json (without core_blocks)
"""

import copy, json, logging, os, re as re2, sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── path setup ──
SCRIPT_DIR = Path(__file__).resolve().parent
KV_DIR = SCRIPT_DIR.parent  # key_version_analysis
RANKING_DIR = KV_DIR / "measure_similarity"

sys.path.insert(0, str(RANKING_DIR))

from similarity import mapBased, tokenBased, treeBased
ALGO_MODULES: Dict[str, Any] = {"mapBased": mapBased, "tokenBased": tokenBased, "treeBased": treeBased}

BASE = KV_DIR / "RQ2.2" / "cases_split" / "dep_rep"


class PatchError(Exception):
    """apply_reverse_patch failed"""
    pass


def parse_case_name(case_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    parts = case_name.split('-')
    for vl in range(1, len(parts)):
        np_ = parts[:-vl]
        joined = '-'.join(np_)
        if joined.count('-') % 2 == 1:
            mid = len(np_) // 2
            return '-'.join(np_[:mid]), '-'.join(np_[mid:]), '-'.join(parts[-vl:])
    return None, None, None


def parse_analysis_md(md_path: Path) -> Tuple[Dict[str, dict], float, str]:
    """Extract delta info, threshold and replacement API name from analysis.md.
    Returns: (deltas_dict, threshold_10pct, replacement_api)
    """
    m = re2.search(r'```json\n(.*?)\n```', md_path.read_text(), re2.DOTALL)
    if not m:
        return {}, 0.0, ""
    data = json.loads(m.group(1))
    threshold = data.get("threshold_10pct", 0.0)
    replacement_api = data.get("replacement_api", "")
    deltas = {}
    for d in data.get("delta", []):
        algo = d.get("algorithm")
        if algo:
            deltas[algo] = {
                "vi1_rank": d.get("vi1_rank"),
                "vi_rank": d.get("vi_rank"),
                "delta": d.get("delta", 0),
                "exceeds_10pct": d.get("exceeds_10pct", False),
            }
    return deltas, threshold, replacement_api


def rank_score_in_candidates(score: float, candidates_without_self: List[dict]) -> int:
    """Insert score into candidate list (minus-self), re-rank, return competition rank."""
    modified = copy.deepcopy(candidates_without_self)
    modified.append({"api_name": "__baseline__", "score": score})
    modified.sort(key=lambda x: -x["score"])
    target_rank = 0
    prev_s = None
    rank = 0
    for i, item in enumerate(modified):
        if item["score"] != prev_s:
            rank = i + 1
            prev_s = item["score"]
        if item["api_name"] == "__baseline__":
            target_rank = rank
    return target_rank


def load_vi_results(case_dir: Path, fix_type: str) -> Tuple[Dict[str, list], Dict[str, list], Dict[str, float], str]:
    """Load Vi and Vi-1 results.
    Returns: (vi_jsons, vi_candidates, vi1_scores, candidate_api)
    """
    result_root = case_dir / "result"
    vi_jsons: Dict[str, list] = {}
    vi1_scores: Dict[str, float] = {}
    candidate_api = ""
    if result_root.is_dir():
        for d in sorted(result_root.iterdir()):
            if d.is_dir() and d.name.startswith("Vi_"):
                for jf in d.glob("*.json"):
                    vi_jsons[jf.stem] = json.loads(jf.read_text())
                break
        for d in sorted(result_root.iterdir()):
            if d.is_dir() and d.name.startswith("Vi-1"):
                d_fqn, r_fqn, _ = parse_case_name(case_dir.name)
                candidate_api = r_fqn or ""
                for jf in d.glob("*.json"):
                    data = json.loads(jf.read_text())
                    for item in data:
                        if item.get("api_name") == candidate_api:
                            vi1_scores[jf.stem] = item["score"]
                            break
                break
    if not candidate_api:
        d_fqn, r_fqn, _ = parse_case_name(case_dir.name)
        candidate_api = r_fqn or ""
    return vi_jsons, vi_jsons, vi1_scores, candidate_api


def apply_reverse_patch(patch_text: str, text: str) -> str:
    lines = text.splitlines(keepends=True)
    result = list(lines)
    plines = patch_text.splitlines(keepends=True)
    i = 0
    while i < len(plines):
        pl = plines[i]
        if pl.startswith('@@'):
            m = re2.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', pl)
            if not m:
                raise PatchError(f"Malformed hunk header: {pl.strip()!r}")
            new_start = int(m.group(3))
            body: List[str] = []
            i += 1
            while i < len(plines):
                pl2 = plines[i]
                if pl2.startswith('@@'): break
                if pl2.startswith(('---', '+++', 'diff ', 'index ')):
                    i += 1; continue
                body.append(pl2)
                i += 1
            new_result = list(lines[:new_start - 1])
            ni = new_start - 1
            for bl in body:
                if not bl: continue
                prefix = bl[0]
                if prefix == ' ':
                    if ni >= len(lines):
                        raise PatchError(f"Line index {ni} out of range (context line)")
                    new_result.append(lines[ni])
                    ni += 1
                elif prefix == '+':
                    if ni >= len(lines):
                        raise PatchError(f"Line index {ni} out of range (added line)")
                    ni += 1
                elif prefix == '-':
                    new_result.append(bl[1:])
            new_result.extend(lines[ni:])
            result = new_result
            lines = new_result
        else:
            i += 1
    return ''.join(result)


def compute_similarity(src_a: str, src_b: str, mod: Any) -> float:
    ra = mod.build_representation(src_a)
    rb = mod.build_representation(src_b)
    return mod.similarity_from_representation(ra, rb)


def analyze_case(case_dir: Path, fix_type: str, cat_param: str, logger: logging.Logger) -> dict:
    res: Dict[str, Any] = {
        "case": case_dir.name, "fix_type": fix_type,
        "cat": cat_param, "error": None,
    }
    ad = case_dir / "diff_analysis"
    if not ad.is_dir():
        logger.warning("  ✗ %s/%s/%s: no diff_analysis directory", fix_type, cat_param, case_dir.name)
        res["error"] = "no diff_analysis"; return res
    new_path = ad / "new.py"
    tgt_path = ad / "target.py"
    if not new_path.exists() or not tgt_path.exists():
        logger.warning("  ✗ %s/%s/%s: missing new.py or target.py", fix_type, cat_param, case_dir.name)
        res["error"] = "missing new.py/target.py"; return res

    new_text = new_path.read_text()
    target_text = tgt_path.read_text()

    # Parse analysis.md → deltas, threshold, replacement API
    deltas, threshold, replacement_api = parse_analysis_md(case_dir / "analysis.md")
    if not deltas:
        logger.warning("  ✗ %s/%s/%s: no delta in analysis.md", fix_type, cat_param, case_dir.name)
        res["error"] = "no delta"; return res
    res["threshold_10pct"] = threshold
    res["delta_vi1_to_vi"] = deltas

    # Threshold-meeting algorithms
    algorithms_meeting = [an for an, d in deltas.items() if d.get("exceeds_10pct", False)]
    res["algorithms_meeting_threshold"] = algorithms_meeting

    # Load Vi and Vi-1 results
    vi_jsons, vi_candidates, vi1_scores, candidate_api = load_vi_results(case_dir, fix_type)
    res["candidate_api"] = candidate_api
    res["algorithms"] = sorted(vi_jsons.keys())
    if not candidate_api or not vi_jsons:
        logger.warning("  ✗ %s/%s/%s: no Vi results or candidate_api", fix_type, cat_param, case_dir.name)
        res["error"] = "no Vi results"; return res

    # Build candidates_without_self
    candidates_without_self: Dict[str, list] = {}
    for an in vi_candidates:
        candidates_without_self[an] = [c for c in vi_candidates[an] if c.get("api_name") != candidate_api]

    # ── Compute baseline rank for all algorithms ──
    baseline: Dict[str, dict] = {}
    for an in sorted(vi_jsons.keys()):
        vi1_score = vi1_scores.get(an)
        if vi1_score is None:
            logger.warning("  ✗ %s/%s/%s: algorithm %s has no Vi-1 score",
                           fix_type, cat_param, case_dir.name, an)
            res["error"] = f"no Vi-1 score for {an}"; return res
        vi_rank = None
        for item in vi_candidates.get(an, []):
            if item.get("api_name") == candidate_api:
                vi_rank = item["rank"]
                break
        bl_rank = rank_score_in_candidates(vi1_score, candidates_without_self.get(an, []))
        baseline[an] = {
            "baseline_score": round(vi1_score, 4),
            "baseline_rank": bl_rank,
            "delta_baseline_to_vi": (bl_rank - vi_rank) if vi_rank is not None else None,
        }
    res["baseline"] = baseline

    # ── Per-block analysis ──
    blocks_list = sorted(ad.glob("block_*.patch"))
    if not blocks_list:
        logger.warning("  ✗ %s/%s/%s: no diff blocks", fix_type, cat_param, case_dir.name)
        res["error"] = "no blocks"; return res

    block_details = []
    for bp in blocks_list:
        bn = bp.stem
        try:
            restored = apply_reverse_patch(bp.read_text(), new_text)
        except PatchError as e:
            logger.warning("  ✗ %s/%s/%s: block %s patch error: %s",
                           fix_type, cat_param, case_dir.name, bn, e)
            res["error"] = f"patch error in {bn}: {e}"; return res

        algo_result: Dict[str, Any] = {}
        for an in sorted(vi_jsons.keys()):
            if an not in ALGO_MODULES:
                raise RuntimeError(
                    f"Algorithm '{an}' not found in ALGO_MODULES. "
                    f"Available: {list(ALGO_MODULES.keys())}"
                )

            try:
                score = compute_similarity(target_text, restored, ALGO_MODULES[an])
            except Exception as e:
                logger.warning("  ✗ %s/%s/%s: similarity failed for %s on block %s: %s",
                               fix_type, cat_param, case_dir.name, an, bn, e)
                res["error"] = f"similarity failed for {an} on {bn}: {e}"; return res

            cws = candidates_without_self.get(an, [])
            restored_rank_val = rank_score_in_candidates(score, cws)

            vi_rank = None
            vi_score_val = None
            for item in vi_candidates.get(an, []):
                if item.get("api_name") == candidate_api:
                    vi_rank = item["rank"]
                    vi_score_val = item["score"]
                    break
            if vi_rank is None:
                logger.warning("  ✗ %s/%s/%s: candidate %s not in Vi for algorithm %s",
                               fix_type, cat_param, case_dir.name, candidate_api, an)
                res["error"] = f"candidate {candidate_api} not in Vi for {an}"; return res

            entry: Dict[str, Any] = {
                "vi_rank": vi_rank,
                "vi_score": round(vi_score_val, 4),
                "restored_score": round(score, 4),
                "restored_rank": restored_rank_val,
                "delta_vi_to_restored": vi_rank - restored_rank_val,
            }
            if an in algorithms_meeting:
                bl = baseline.get(an, {})
                if bl.get("baseline_rank") is not None:
                    entry["distance_to_baseline"] = abs(restored_rank_val - bl["baseline_rank"])
            algo_result[an] = entry

        block_details.append({"block": bn, "patch_ok": True, "algorithms": algo_result})

    res["blocks"] = block_details

    return res


def main():
    log_path = SCRIPT_DIR / "analyze_fix_D_blocks.log"
    log_fh = open(str(log_path), 'a', buffering=1)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(log_fh),
            logging.StreamHandler(sys.stdout),
        ],
    )
    logger = logging.getLogger(__name__)

    ok_count = 0
    skip_count = 0
    for fix_type in ["fix_D"]:
        for cons in ["consistent", "no_consistent"]:
            for cat in ["class", "function", "method"]:
                cat_dir = BASE / fix_type / cons / cat
                if not cat_dir.is_dir():
                    continue
                for case_dir in sorted(cat_dir.iterdir()):
                    if not case_dir.is_dir():
                        continue
                    logger.info("→ %s/%s/%s", fix_type, cat, case_dir.name)
                    res = analyze_case(case_dir.resolve(), fix_type, cat, logger)
                    err = res.get("error")
                    if err:
                        skip_count += 1
                    else:
                        ok_count += 1

                    if not err:
                        ad_path = case_dir.resolve() / "diff_analysis"
                        if ad_path.is_dir():
                            out = {
                                "case": res["case"], "fix_type": res["fix_type"],
                                "candidate_api": res.get("candidate_api", ""),
                                "error": res.get("error"),
                                "threshold_10pct": res.get("threshold_10pct", 0),
                                "algorithms_meeting_threshold": res.get("algorithms_meeting_threshold", []),
                                "delta_vi1_to_vi": res.get("delta_vi1_to_vi", {}),
                                "algorithms": res.get("algorithms", []),
                                "baseline": res.get("baseline", {}),
                                "blocks": [],
                            }
                            for bd in res.get("blocks", []):
                                bd_out = {
                                    "block": bd["block"], "patch_ok": bd.get("patch_ok", False),
                                    "algorithms": {},
                                }
                                for an, adata in bd.get("algorithms", {}).items():
                                    if "error" in adata:
                                        bd_out["algorithms"][an] = {"error": adata["error"]}
                                    else:
                                        entry = {
                                            "vi_rank": adata["vi_rank"], "vi_score": adata["vi_score"],
                                            "restored_score": adata["restored_score"],
                                            "restored_rank": adata["restored_rank"],
                                            "delta_vi_to_restored": adata["delta_vi_to_restored"],
                                        }
                                        if "distance_to_baseline" in adata:
                                            entry["distance_to_baseline"] = adata["distance_to_baseline"]
                                        bd_out["algorithms"][an] = entry
                                out["blocks"].append(bd_out)
                            (ad_path / "block_analysis.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))

    logger.info("Done: %d ok, %d skipped, %d total", ok_count, skip_count, ok_count + skip_count)
    log_fh.close()


if __name__ == "__main__":
    main()
