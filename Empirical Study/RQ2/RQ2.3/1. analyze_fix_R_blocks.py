#!/usr/bin/env python3
"""
fix_R Diff Block analysis (parallel):
  For dep_rep, candidates_cause, common_cause fix_R cases:
  1. baseline_rank = Vi-1 rank (read from analysis.md, no recomputation needed)
  2. For each block: reverse patch → restored deprecated API code
  3. Compute similarity of restored vs ALL candidates in R_candidates → find rank
  Output: diff_analysis/block_analysis.json (without core_blocks)
"""

import json, os, re as re2, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── path setup ──
SCRIPT_DIR = Path(__file__).resolve().parent
KV_DIR = SCRIPT_DIR.parent
RANKING_DIR = KV_DIR / "measure_similarity"

sys.path.insert(0, str(RANKING_DIR))

from similarity import mapBased, tokenBased
from similarity import treeBased

algo_mods: Dict[str, Any] = {"mapBased": mapBased, "tokenBased": tokenBased, "treeBased": treeBased}

BASE_PATHS = [
    KV_DIR / "RQ2.2" / "cases_split" / "dep_rep" / "fix_R",
    KV_DIR / "RQ2.2" / "cases_split" / "candidates_cause" / "fix_R",
    KV_DIR / "RQ2.2" / "cases_split" / "common_cause" / "fix_R",
]
MAX_WORKERS = min(80, os.cpu_count() or 1, 61)

SIM_POOL: Optional[ProcessPoolExecutor] = None


def init_sim_worker():
    """Worker init: import similarity modules once per process."""
    import sys as sys_w
    sys_w.path.insert(0, str(RANKING_DIR))
    global mapBased_w, tokenBased_w, treeBased_w
    from similarity import mapBased as mapBased_w
    from similarity import tokenBased as tokenBased_w
    from similarity import treeBased as treeBased_w


def compute_one_similarity(args):
    """Compute single similarity in worker process (algo_name, restored_rep, cand_rep) → float"""
    algo_name, restored_rep, cand_rep = args
    mod = {"mapBased": mapBased_w, "tokenBased": tokenBased_w, "treeBased": treeBased_w}.get(algo_name)
    if mod is None:
        return -1.0
    try:
        return mod.similarity_from_representation(restored_rep, cand_rep)
    except Exception:
        return -1.0


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
    """Extract deltas, threshold and replacement API from analysis.md."""
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


def apply_reverse_patch(patch_text: str, text: str) -> Optional[str]:
    lines = text.splitlines(keepends=True)
    result = list(lines)
    plines = patch_text.splitlines(keepends=True)
    i = 0
    while i < len(plines):
        pl = plines[i]
        if pl.startswith('@@'):
            m = re2.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', pl)
            if not m:
                i += 1; continue
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
                    if ni >= len(lines): return None
                    new_result.append(lines[ni])
                    ni += 1
                elif prefix == '+':
                    if ni >= len(lines): return None
                    ni += 1
                elif prefix == '-':
                    new_result.append(bl[1:])
            new_result.extend(lines[ni:])
            result = new_result
            lines = new_result
        else:
            i += 1
    return ''.join(result)


def rank_in_scores(scores: Dict[str, float], target_name: str) -> int:
    """Given {api_name: score}, return competition rank of target_name."""
    sorted_items = sorted(scores.items(), key=lambda x: -x[1])
    prev_score = None
    rank = 0
    for i, (name, score) in enumerate(sorted_items):
        if score != prev_score:
            rank = i + 1
            prev_score = score
        if name == target_name:
            return rank
    return 0


def worker(case_dir_str: str) -> Tuple[str, Optional[str]]:
    """Process a single case (called sequentially, inner similarity parallelized)."""
    case_dir = Path(case_dir_str)
    cn = case_dir.name
    t0 = time.time()

    def _log(msg: str) -> None:
        elapsed = time.time() - t0
        print(f"  [{elapsed:5.1f}s] {cn} | {msg}", file=sys.stderr, flush=True)

    ana_path = case_dir / "analysis.md"
    if not ana_path.exists():
        return (cn, "no analysis.md")
    deltas, threshold, replacement_api = parse_analysis_md(ana_path)
    if not deltas:
        return (cn, "no delta")
    algorithms_meeting = [an for an, d in deltas.items() if d.get("exceeds_10pct", False)]

    rc_dir = case_dir / "R_candidates"
    if not rc_dir.is_dir():
        return (cn, "no R_candidates")
    rc_subdirs = [d for d in rc_dir.iterdir() if d.is_dir() or d.is_symlink()]
    if not rc_subdirs:
        return (cn, "no R_candidates subdir")
    rc_ver_dir = rc_subdirs[0]

    ad = case_dir / "diff_analysis"
    if not ad.is_dir():
        return (cn, "no diff_analysis")
    new_path = ad / "new.py"
    if not new_path.exists():
        return (cn, "no new.py")
    new_text = new_path.read_text()

    cand_files = sorted(rc_ver_dir.glob("*.py"))
    if not cand_files:
        return (cn, "no candidate .py files")
    cand_names = [cf.stem for cf in cand_files]

    blocks = sorted(ad.glob("block_*.patch"))
    if not blocks:
        return (cn, "no blocks")

    _log(f"start: algos={sorted(deltas.keys())} candidates={len(cand_files)} "
         f"blocks={len(blocks)} replacement={replacement_api} "
         f"threshold_10pct={threshold:.1f} meeting={algorithms_meeting}")

    # Pre-compute all candidate representations
    fatal_error: Optional[str] = None
    cached: Dict[str, Dict[str, Any]] = {}
    for an in sorted(deltas.keys()):
        mod = algo_mods.get(an)
        if not mod:
            continue
        cached[an] = {}
        rep_failures = 0
        for cf in cand_files:
            try:
                src = cf.read_text()
                cached[an][cf.stem] = mod.build_representation(src)
            except Exception:
                rep_failures += 1
        if rep_failures > 0:
            fatal_error = f"candidate rep build failed: algo={an} {rep_failures}/{len(cand_files)}"
            break
        _log(f"  algo={an} reps built: {len(cached[an])}/{len(cand_files)}")

    if fatal_error:
        return (cn, fatal_error)
    if not cached:
        return (cn, "no cached representations")

    # Vi and Vi-1 results
    result_root = case_dir / "result"
    vi_data: Dict[str, list] = {}
    vi1_data: Dict[str, list] = {}
    if result_root.is_dir():
        for d in sorted(result_root.iterdir()):
            if d.is_dir() and d.name.startswith("Vi_"):
                for jf in d.glob("*.json"):
                    vi_data[jf.stem] = json.loads(jf.read_text())
                break
        for d in sorted(result_root.iterdir()):
            if d.is_dir() and d.name.startswith("Vi-1"):
                for jf in d.glob("*.json"):
                    vi1_data[jf.stem] = json.loads(jf.read_text())
                break

    # Baseline: baseline_rank = vi1_rank
    baseline: Dict[str, dict] = {}
    for an in sorted(deltas.keys()):
        d = deltas[an]
        vi1_r = d["vi1_rank"]
        vi_r = d["vi_rank"]
        vi1_score = None
        for item in vi1_data.get(an, []):
            if item.get("api_name") == replacement_api:
                vi1_score = item["score"]
                break
        baseline[an] = {
            "baseline_score": round(vi1_score, 4) if vi1_score else None,
            "baseline_rank": vi1_r,
            "delta_baseline_to_vi": (vi1_r - vi_r) if vi_r is not None else None,
        }

    block_details = []
    for bi, bp in enumerate(blocks):
        if fatal_error:
            break
        bn = bp.stem
        restored = apply_reverse_patch(bp.read_text(), new_text)
        if restored is None:
            block_details.append({"block": bn, "patch_ok": False, "algorithms": {}})
            continue

        algo_result: Dict[str, Any] = {}
        try:
            for an in sorted(deltas.keys()):
                if fatal_error:
                    break
                mod = algo_mods.get(an)
                ar = cached.get(an)
                if not mod or not ar:
                    algo_result[an] = {"error": "unavailable"}
                    continue

                try:
                    restored_rep = mod.build_representation(restored)
                except Exception as e:
                    fatal_error = f"block[{bi+1}] {bn} algo={an} build_rep failed: {e}"
                    break

                if SIM_POOL is None:
                    fatal_error = f"block[{bi+1}] {bn} algo={an} pool unavailable"
                    break
                fut_to_name = {}
                for cand_name, cand_rep in ar.items():
                    fut = SIM_POOL.submit(compute_one_similarity, (an, restored_rep, cand_rep))
                    fut_to_name[fut] = cand_name
                scores: Dict[str, float] = {}
                ok_sim = 0
                sim_failures = 0
                for fut in as_completed(fut_to_name):
                    cand_name = fut_to_name[fut]
                    try:
                        s = fut.result()
                    except Exception:
                        s = -1.0
                    if s >= 0:
                        scores[cand_name] = s
                        ok_sim += 1
                    else:
                        sim_failures += 1

                if sim_failures > 0:
                    fatal_error = (f"block[{bi+1}] {bn} algo={an} sim failures: "
                                   f"{ok_sim}/{len(fut_to_name)} ok, {sim_failures} failed")
                    break

                if replacement_api not in scores:
                    fatal_error = f"block[{bi+1}] {bn} algo={an} replacement API not in scores"
                    break

                restored_rank_val = rank_in_scores(scores, replacement_api)
                restored_score_val = scores[replacement_api]

                d = deltas.get(an, {})
                vi_rank = d.get("vi_rank")
                vi_score_val = None
                for item in vi_data.get(an, []):
                    if item.get("api_name") == replacement_api:
                        vi_score_val = item["score"]
                        break

                entry: Dict[str, Any] = {
                    "vi_rank": vi_rank,
                    "vi_score": round(vi_score_val, 4) if vi_score_val else None,
                    "restored_score": round(restored_score_val, 4),
                    "restored_rank": restored_rank_val,
                    "delta_vi_to_restored": (vi_rank - restored_rank_val) if vi_rank is not None else None,
                }
                if an in algorithms_meeting:
                    bl_r = baseline.get(an, {}).get("baseline_rank")
                    if bl_r is not None:
                        entry["distance_to_baseline"] = abs(restored_rank_val - bl_r)
                algo_result[an] = entry

            if fatal_error:
                break
            block_details.append({"block": bn, "patch_ok": True, "algorithms": algo_result})
        except Exception as e:
            fatal_error = f"block[{bi+1}] {bn} processing error: {e}"
            break

    if fatal_error:
        return (cn, fatal_error)

    out = {
        "case": cn, "fix_type": "fix_R",
        "candidate_api": replacement_api,
        "error": None,
        "threshold_10pct": threshold,
        "algorithms_meeting_threshold": algorithms_meeting,
        "delta_vi1_to_vi": deltas,
        "algorithms": sorted(deltas.keys()),
        "baseline": baseline,
        "blocks": block_details,
    }
    out_path = ad / "block_analysis.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return (cn, None)


def main():
    tasks = []
    for base in BASE_PATHS:
        if not base.is_dir():
            continue
        for cons_name in os.listdir(base):
            cons_dir = base / cons_name
            if not cons_dir.is_dir():
                continue
            for cat in ["class", "function", "method"]:
                cat_dir = cons_dir / cat
                if not cat_dir.is_dir():
                    continue
                for case_dir in sorted(cat_dir.iterdir()):
                    if not case_dir.is_dir():
                        continue
                    tasks.append(str(case_dir.resolve()))

    print(f"Processing {len(tasks)} fix_R cases "
          f"(inner {MAX_WORKERS} concurrent similarity workers)")
    start = time.time()
    done = ok = err_count = 0

    global SIM_POOL
    with ProcessPoolExecutor(max_workers=MAX_WORKERS, initializer=init_sim_worker) as SIM_POOL:
        print(f"[pool] {MAX_WORKERS} worker pool created", file=sys.stderr, flush=True)
        for t in tasks:
            cn, error = worker(t)
            done += 1
            if error:
                err_count += 1
                tag = f"[ERR] {error}"
            else:
                ok += 1
                tag = "[OK]"
            elapsed = time.time() - start
            print(f"[{done}/{len(tasks)}] {tag} {cn} ({elapsed:.0f}s)")

    print(f"\nDone: {ok} OK, {err_count} errors, "
          f"total {ok + err_count}/{len(tasks)} elapsed {time.time()-start:.0f}s")


if __name__ == "__main__":
    main()
