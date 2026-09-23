"""
功能说明：
    three_routes 版相似度排序脚本。

    主流程与 /media/he/Rbench/similarity/rank.py 基本一致：
    - 遍历 root/libname/cur
    - 对每个 cur 运行 tokenBased / treeBased / mapBased 三种算法
    - 生成 result/.../*.json

    差异点：
    - 每个 cur 读取 compare_versions.json（由 three_routes/construct_compares.py 生成）
    - compare_versions.json 内包含 3 个实验（fix_D / fix_D_t / fix_R）的 queries/candidates 版本集合与 enabled 标记
    - enabled=false 的实验将被跳过，不做扫描与计算
    - 输出按实验隔离：cur/result/<experiment>/<query>-<candidate>/<algorithm>.json

全局配置说明：
    本脚本复用 rank.py 的核心实现，因此其全局配置同样生效：
    - rank.RANK_WORKER_MAX_TASKS：candidate 子进程最大复用任务数
    - rank.CANDIDATES_WORKERS：candidate 子进程池并发上限

    你可以通过本脚本的命令行参数覆盖上述两个值。
"""

from __future__ import annotations

import argparse
import gc
import json
import logging
import os
import sys
import time
import traceback
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple

import multiprocessing as mp

from similarity.mapBased import (
    build_representation as map_build_representation,
    similarity_from_representation as map_similarity_from_representation,
)
from similarity.tokenBased import (
    build_representation as token_build_representation,
    similarity_from_representation as token_similarity_from_representation,
)
from similarity.treeBased import (
    build_representation as tree_build_representation,
    similarity_from_representation as tree_similarity_from_representation,
)

RANK_WORKER_MAX_TASKS = 2
CANDIDATES_WORKERS = 80


def setup_logger(
    log_file: Path,
    logger_name: str = "similarity_rank_logger",
    enable_console: bool = False,
    file_mode: str = "a",
) -> logging.Logger:
    """
    功能说明：
        创建并配置日志记录器。
        日志会输出到指定日志文件；
        当 enable_console=True 时，也会同时输出到控制台。

    参数说明：
        log_file:
            日志文件路径，类型为 Path。

        logger_name:
            日志记录器名称。
            不同名称可创建不同 logger，避免多个流程共用同一个 logger。

        enable_console:
            是否同时输出到控制台。
            True 表示输出到控制台和文件；
            False 表示仅输出到文件。

        file_mode:
            日志文件打开模式。
            常用值：
            - "a"：追加
            - "w"：覆盖

    返回说明：
        配置完成的 logger 对象。
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    log_file.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode=file_mode)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def validate_similarity_score(score: Any, api_name: str) -> float:
    """
    功能说明：
        校验相似度分数是否合法，并转成 float。

    参数说明：
        score:
            similarity_from_representation 返回的分数。

        api_name:
            当前候选 API 名称，用于报错定位。

    返回说明：
        合法的 float 分数。

    异常说明：
        - TypeError：返回值不是数值
        - ValueError：返回值不在 [0, 1] 区间
    """
    if not isinstance(score, (int, float)):
        raise TypeError(f"相似度函数对候选项 {api_name} 返回的分数不是数值类型：{type(score)}")

    score = float(score)

    if not (0 <= score <= 1):
        raise ValueError(f"相似度函数对候选项 {api_name} 返回的分数 {score} 不在 [0, 1] 区间内")

    return score


def get_algorithm_registry() -> Dict[str, Dict[str, Callable[..., Any]]]:
    """
    功能说明：
        返回三个相似度算法的统一注册表。

    参数说明：
        无。

    返回说明：
        {
            "mapBased": {
                "build": ...,
                "compare": ...
            },
            "tokenBased": {
                "build": ...,
                "compare": ...
            },
            "treeBased": {
                "build": ...,
                "compare": ...
            }
        }
    """
    return {
        "mapBased": {
            "build": map_build_representation,
            "compare": map_similarity_from_representation,
        },
        "tokenBased": {
            "build": token_build_representation,
            "compare": token_similarity_from_representation,
        },
        "treeBased": {
            "build": tree_build_representation,
            "compare": tree_similarity_from_representation,
        },
    }


def finalize_ranked_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    功能说明：
        对结果按 score 降序排序。
        若分数相同，则按 candidate_order 升序稳定排序，并使用竞赛排名补充 rank 字段。
        竞赛排名规则为：同分同排名，后续排名按实际位置跳号（例如 1，1，3）。
        candidate_order 仅用于内部稳定排序，不会写入最终输出。

    参数说明：
        results:
            未排序结果列表，元素格式为：
            {
                "api_name": ...,
                "score": ...,
                "candidate_order": ...
            }

    返回说明：
        排序并补 rank 后的结果列表。
    """
    results.sort(key=lambda x: (-x["score"], x.get("candidate_order", 10**18)))

    previous_score: Optional[float] = None
    previous_rank = 0
    for idx, item in enumerate(results, start=1):
        if idx == 1 or item["score"] != previous_score:
            previous_rank = idx
        item.pop("candidate_order", None)
        item["rank"] = previous_rank
        previous_score = item["score"]

    return results


def read_text_file(file_path: Path) -> str:
    """
    功能说明：
        读取指定路径下文本文件的全部内容。

    参数说明：
        file_path:
            待读取文件的路径，类型为 Path。

    返回说明：
        文件内容字符串。

    异常说明：
        - 如果文件不存在，则抛出 FileNotFoundError
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    return file_path.read_text(encoding="utf-8")


def split_cur_name(cur_name: str) -> Tuple[str, str]:
    """
    功能说明：
        按 '-' 对 cur 的最后一级目录名进行分隔。

        分隔规则：
        1. 如果只有 1 个 '-'，则直接按该 '-' 分成两段
        2. 如果有多个 '-'，则 '-' 的数量必须为奇数，
           并以中间那个 '-' 作为分隔点，分成两段

    参数说明：
        cur_name:
            cur 的最后一级目录名字符串。

    返回说明：
        一个二元组：
        (
            D_fqn,
            R_fqn
        )

    异常说明：
        - 如果不包含 '-'，则抛出 ValueError
        - 如果 '-' 数量大于 1 且不是奇数，则抛出 ValueError
    """
    hyphen_count = cur_name.count("-")

    if hyphen_count == 0:
        raise ValueError(f"cur 的最后一级目录名不包含 '-'：{cur_name}")

    if hyphen_count == 1:
        left, right = cur_name.split("-", 1)
        return left, right

    if hyphen_count % 2 == 0:
        raise ValueError(f"cur 的最后一级目录名中 '-' 数量大于 1 时必须为奇数，当前为 {hyphen_count}：{cur_name}")

    split_index = hyphen_count // 2 + 1
    parts = cur_name.split("-", split_index)

    left = "-".join(parts[:split_index])
    right = parts[split_index]

    return left, right


def compile_query_representations(
    query_code_map: Dict[str, str],
    algorithm_name: str,
    cur_name: str,
    logger: logging.Logger,
) -> Tuple[Dict[str, Any], List[str]]:
    """
    功能说明：
        使用指定算法，将所有 query 版本源码编译为可复用表示。
        若某个 query 编译失败，会记录错误并跳过该 query，保证后续流程继续执行。

    参数说明：
        query_code_map:
            查询版本源码字典，例如：
            {
                "Vn": "...",
                "Va-1": "...",
                "Vd-1": "..."
            }

        algorithm_name:
            算法名称。

        cur_name:
            当前 cur 的目录名，用于生成统一的 5 段式错误行。

        logger:
            日志记录器。

    返回说明：
        (compiled_query_map, error_lines)

        compiled_query_map:
            编译后的 query 表示字典：
            {
                "Vn": compiled_repr,
                "Va-1": compiled_repr,
                ...
            }

        error_lines:
            5 段式错误行列表，格式为：
            [cur名] | [query标签] | [算法] | [阶段] | [简短报错原因]
    """
    registry = get_algorithm_registry()
    if algorithm_name not in registry:
        raise ValueError(f"不支持的算法名称：{algorithm_name}")

    build_func = registry[algorithm_name]["build"]
    compiled_query_map: Dict[str, Any] = {}
    error_lines: List[str] = []

    for query_label, query_code in query_code_map.items():
        logger.info("开始编译 query：algorithm=%s, query=%s", algorithm_name, query_label)
        try:
            compiled_query_map[query_label] = build_func(query_code)
            logger.info("query 编译完成：algorithm=%s, query=%s", algorithm_name, query_label)
        except Exception as e:
            clean_error_msg = str(e).replace("\n", " ").replace("\r", "")
            error_line = f"{cur_name} | {query_label} | {algorithm_name} | query_build | {clean_error_msg}"
            error_lines.append(error_line)

            logger.error(
                "query 编译失败，已跳过：algorithm=%s, query=%s, error=%s",
                algorithm_name,
                query_label,
                str(e),
            )
            logger.error("详细堆栈信息：\n%s", traceback.format_exc())

    return compiled_query_map, error_lines


def rank_one_candidate_worker(
    compiled_queries: Dict[str, Any],
    candidate_item: Tuple[str, Path, int],
    algorithm_name: str,
) -> Dict[str, Any]:
    """
    功能说明：
        在子进程中处理单个 candidate：
        1. 动态读取文件内容
        2. 编译 candidate
        3. 与多个 compiled query 分别计算相似度
        4. 返回该 candidate 的结果和错误信息

    参数说明：
        compiled_queries:
            已编译 query 表示字典。

        candidate_item:
            单个候选项：
            (api_name, candidate_file_path, candidate_order)

        algorithm_name:
            算法名称。

    返回说明：
        {
            "success": True/False,
            "api_name": "...",
            "result_items": {
                "Vn": {"api_name": "...", "score": ...} 或 None,
                "Va-1": {"api_name": "...", "score": ...} 或 None,
                ...
            },
            "errors": [
                {
                    "stage": "build" / "compare",
                    "api_name": "...",
                    "query_label": "..." 或 None,
                    "error": "...",
                    "traceback": "..."
                },
                ...
            ],
            "count": 1
        }
    """
    registry = get_algorithm_registry()
    if algorithm_name not in registry:
        raise ValueError(f"不支持的算法名称：{algorithm_name}")

    build_func = registry[algorithm_name]["build"]
    compare_func = registry[algorithm_name]["compare"]

    if not compiled_queries:
        raise ValueError("compiled_queries 不能为空")

    api_name, py_file, candidate_order = candidate_item
    result_items: Dict[str, Any] = {query_label: None for query_label in compiled_queries.keys()}
    errors: List[Dict[str, Any]] = []

    try:
        try:
            candidate_code = py_file.read_text(encoding="utf-8")
            compiled_candidate = build_func(candidate_code)
        except Exception as e:
            errors.append(
                {
                    "stage": "build",
                    "api_name": api_name,
                    "query_label": None,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
            )
            return {
                "success": True,
                "api_name": api_name,
                "result_items": result_items,
                "errors": errors,
                "count": 1,
            }

        try:
            for query_label, compiled_query in compiled_queries.items():
                try:
                    score = compare_func(compiled_query, compiled_candidate)
                    score = validate_similarity_score(score, api_name)
                    result_items[query_label] = {
                        "api_name": api_name,
                        "score": score,
                        "candidate_order": candidate_order,
                    }
                except Exception as e:
                    errors.append(
                        {
                            "stage": "compare",
                            "api_name": api_name,
                            "query_label": query_label,
                            "error": str(e),
                            "traceback": traceback.format_exc(),
                        }
                    )
        finally:
            del compiled_candidate
            gc.collect()

        return {
            "success": True,
            "api_name": api_name,
            "result_items": result_items,
            "errors": errors,
            "count": 1,
        }

    except Exception as e:
        return {
            "success": False,
            "api_name": api_name,
            "result_items": result_items,
            "errors": errors,
            "count": 1,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


def rank_candidates_by_similarity(
    compiled_queries: Dict[str, Any],
    candidate_dir: Path,
    algorithm_name: str,
    cur_name: str,
    logger: logging.Logger,
) -> Tuple[Dict[str, List[Dict[str, Any]]], List[str]]:
    """
    功能说明：
        对一个 candidate 版本进行统一处理：
        1. 传入若干个“已编译好的 query 表示”
        2. 扫描目录获取所有的 .py 文件
        3. 使用指定大小的进程池，将每个 candidate 作为一个独立任务并发处理
        4. 父进程汇总所有任务结果，并按 query_label 返回未排序结果

    参数说明：
        compiled_queries:
            已编译的 query 表示字典。

        candidate_dir:
            候选源码目录路径。

        algorithm_name:
            算法名称：
            "mapBased" / "tokenBased" / "treeBased"

        cur_name:
            当前 cur 的目录名，用于在错误日志中定位用例。

        logger:
            日志记录器。

    返回说明：
        一个字典，key 为 query_label，value 为该 query 对应的未排序结果列表。
    """
    registry = get_algorithm_registry()
    if algorithm_name not in registry:
        raise ValueError(f"不支持的算法名称：{algorithm_name}")

    if not compiled_queries:
        raise ValueError("compiled_queries 不能为空")

    result_map: Dict[str, List[Dict[str, Any]]] = {query_label: [] for query_label in compiled_queries.keys()}
    all_error_lines: List[str] = []

    candidate_items: List[Tuple[str, Path, int]] = []
    if candidate_dir.is_dir():
        for idx, py_file in enumerate(sorted(candidate_dir.glob("*.py"), key=lambda p: p.name), start=1):
            candidate_items.append((py_file.stem, py_file, idx))

    total_candidates = len(candidate_items)
    logger.info(
        "开始 rank 计算：algorithm=%s, query_count=%d, candidate_count=%d",
        algorithm_name,
        len(compiled_queries),
        total_candidates,
    )

    if total_candidates == 0:
        logger.info("candidate 为空，直接返回空结果：algorithm=%s", algorithm_name)
        return result_map, []

    if CANDIDATES_WORKERS < 0:
        raise ValueError(f"CANDIDATES_WORKERS 必须 >= 0，当前为：{CANDIDATES_WORKERS}")

    if CANDIDATES_WORKERS == 0:
        cpu_count = os.cpu_count() or 1
        max_workers = min(total_candidates, cpu_count)
    else:
        max_workers = min(total_candidates, CANDIDATES_WORKERS)

    max_workers = max(1, max_workers)

    logger.info(
        "rank 子进程配置：algorithm=%s, candidate_count=%d, max_workers=%d, max_tasks_per_child=%d",
        algorithm_name,
        total_candidates,
        max_workers,
        RANK_WORKER_MAX_TASKS,
    )

    with ProcessPoolExecutor(
        max_workers=max_workers,
        max_tasks_per_child=RANK_WORKER_MAX_TASKS,
        mp_context=mp.get_context("spawn"),
    ) as executor:
        candidate_iter = iter(candidate_items)
        inflight_limit = max_workers * 2
        future_to_candidate_meta: Dict[Any, Tuple[str, int]] = {}

        def submit_next() -> None:
            api_name, py_file, candidate_order = next(candidate_iter)
            fut = executor.submit(
                rank_one_candidate_worker,
                compiled_queries,
                (api_name, py_file, candidate_order),
                algorithm_name,
            )
            future_to_candidate_meta[fut] = (api_name, candidate_order)

        for _ in range(min(inflight_limit, total_candidates)):
            submit_next()

        while future_to_candidate_meta:
            done, _ = wait(future_to_candidate_meta, return_when=FIRST_COMPLETED)
            for fut in done:
                api_name, candidate_order = future_to_candidate_meta.pop(fut)

                try:
                    one_result = fut.result()
                except Exception as e:
                    clean_error_msg = str(e).replace("\n", " ").replace("\r", "")
                    error_line = f"{cur_name} | {api_name} | {algorithm_name} | worker | {clean_error_msg}"
                    all_error_lines.append(error_line)

                    logger.error(
                        "candidate 子进程异常，已跳过：algorithm=%s, api_name=%s, candidate_order=%d, error=%s",
                        algorithm_name,
                        api_name,
                        candidate_order,
                        str(e),
                    )
                    logger.error("详细堆栈信息：\n%s", traceback.format_exc())
                else:
                    if not one_result.get("success", False):
                        clean_error_msg = str(one_result.get("error", "")).replace("\n", " ").replace("\r", "")
                        error_line = f"{cur_name} | {api_name} | {algorithm_name} | worker | {clean_error_msg}"
                        all_error_lines.append(error_line)

                        logger.error(
                            "candidate 任务失败：algorithm=%s, api_name=%s, candidate_order=%d, error=%s",
                            algorithm_name,
                            api_name,
                            candidate_order,
                            one_result.get("error"),
                        )
                        if one_result.get("traceback"):
                            logger.error("详细堆栈信息：\n%s", one_result["traceback"])

                    for query_label, item in one_result.get("result_items", {}).items():
                        if item is not None:
                            result_map[query_label].append(item)

                    for err in one_result.get("errors", []):
                        stage = err.get("stage")
                        api_name = err.get("api_name")
                        query_label = err.get("query_label")
                        error_msg = err.get("error", "")
                        tb = err.get("traceback")

                        clean_error_msg = str(error_msg).replace("\n", " ").replace("\r", "")
                        error_line = f"{cur_name} | {api_name} | {algorithm_name} | {stage} | {clean_error_msg}"
                        all_error_lines.append(error_line)

                        if stage == "build":
                            logger.error(
                                "candidate 编译失败，已跳过：algorithm=%s, api_name=%s, error=%s",
                                algorithm_name,
                                api_name,
                                error_msg,
                            )
                        else:
                            logger.error(
                                "相似度计算失败，已跳过：algorithm=%s, query=%s, api_name=%s, error=%s",
                                algorithm_name,
                                query_label,
                                api_name,
                                error_msg,
                            )

                        if tb:
                            logger.error("详细堆栈信息：\n%s", tb)

                try:
                    submit_next()
                except StopIteration:
                    pass

    logger.info(
        "rank 计算完成：algorithm=%s, query_count=%d, candidate_count=%d",
        algorithm_name,
        len(compiled_queries),
        total_candidates,
    )

    gc.collect()
    return result_map, all_error_lines


def stable_unique(items: Sequence[str]) -> List[str]:
    """
    功能说明：
        对字符串序列做稳定去重，保留首次出现顺序。

    参数说明：
        items:
            输入序列。

    返回说明：
        去重后的列表。
    """
    seen: Set[str] = set()
    out: List[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def load_compare_plan(compare_file: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    功能说明：
        读取并解析 compare_versions.json。

    参数说明：
        compare_file:
            compare_versions.json 的路径。

    返回说明：
        (plan, error)
        - plan: 解析后的 dict；若失败为 None
        - error: 失败原因；若成功为 None
    """
    if not compare_file.is_file():
        return None, f"compare_versions.json not found: {compare_file}"
    try:
        plan = json.loads(compare_file.read_text(encoding="utf-8"))
    except Exception as e:
        return None, f"compare_versions.json invalid json: {str(e)}"
    if not isinstance(plan, dict):
        return None, "compare_versions.json root is not an object"
    return plan, None


def normalize_experiment_names(names: Optional[str]) -> Set[str]:
    """
    功能说明：
        解析并校验 --only-experiments 参数。

    参数说明：
        names:
            逗号分隔的实验名字符串，如 "fix_D,fix_R"；None 表示默认全选。

    返回说明：
        实验名集合。
    """
    if not names:
        return {"fix_D", "fix_D_t", "fix_R"}
    parts = [p.strip() for p in names.split(",")]
    parts = [p for p in parts if p]
    allowed = {"fix_D", "fix_D_t", "fix_R"}
    bad = [p for p in parts if p not in allowed]
    if bad:
        raise ValueError(f"--only-experiments 包含不支持的实验名：{bad}，仅支持：{sorted(allowed)}")
    return set(parts)


def extract_experiment_spec(plan: Dict[str, Any], exp_name: str) -> Dict[str, Any]:
    """
    功能说明：
        从 compare_versions.json 中读取某个实验的配置，并规范化字段类型。

    参数说明：
        plan:
            compare_versions.json 的根对象 dict。

        exp_name:
            实验名：fix_D / fix_D_t / fix_R。

    返回说明：
        统一格式的实验配置：
        {
            "enabled": bool,
            "query": Optional[str],
            "queries": List[str],
            "candidate": Optional[str],
            "candidates": List[str],
            "reason": str
        }
    """
    experiments = plan.get("experiments", {})
    if not isinstance(experiments, dict):
        return {
            "enabled": False,
            "query": None,
            "queries": [],
            "candidate": None,
            "candidates": [],
            "reason": "compare_versions.json missing experiments",
        }
    spec = experiments.get(exp_name, {})
    if not isinstance(spec, dict):
        return {
            "enabled": False,
            "query": None,
            "queries": [],
            "candidate": None,
            "candidates": [],
            "reason": f"compare_versions.json experiments.{exp_name} not an object",
        }

    enabled = bool(spec.get("enabled", False))
    query = spec.get("query", None)
    candidate = spec.get("candidate", None)

    queries = spec.get("queries", [])
    if not isinstance(queries, list):
        queries = []
    queries = [str(x).strip() for x in queries if str(x).strip()]

    candidates = spec.get("candidates", [])
    if not isinstance(candidates, list):
        candidates = []
    candidates = [str(x).strip() for x in candidates if str(x).strip()]

    reason = str(spec.get("reason", "") or "")

    return {
        "enabled": enabled,
        "query": str(query).strip() if isinstance(query, str) and query.strip() else None,
        "queries": stable_unique(queries),
        "candidate": str(candidate).strip() if isinstance(candidate, str) and candidate.strip() else None,
        "candidates": stable_unique(candidates),
        "reason": reason,
    }


def resolve_versions_for_experiment(exp_name: str, spec: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """
    功能说明：
        将实验配置转换为 (query_labels, candidate_labels)。

    参数说明：
        exp_name:
            实验名。

        spec:
            extract_experiment_spec 返回的规范化实验配置。

    返回说明：
        (query_labels, candidate_labels)
        - query_labels: 需要读取 base_dir/<D_fqn>/<label>.py 的 label 列表
        - candidate_labels: 需要读取 base_dir/R_candidates/<label>/ 的 label 列表
    """
    if exp_name in {"fix_D", "fix_D_t"}:
        query = spec.get("query")
        queries = [query] if isinstance(query, str) and query else []
        candidates = spec.get("candidates", [])
        return stable_unique([q for q in queries if q]), stable_unique([c for c in candidates if c])
    if exp_name == "fix_R":
        queries = spec.get("queries", [])
        candidate = spec.get("candidate")
        candidates = [candidate] if isinstance(candidate, str) and candidate else []
        return stable_unique([q for q in queries if q]), stable_unique([c for c in candidates if c])
    raise ValueError(f"未知实验名：{exp_name}")


def validate_query_files(base_dir: Path, d_fqn: str, query_labels: List[str]) -> Tuple[List[str], List[str]]:
    """
    功能说明：
        校验 query 版本文件是否存在，并分离可用与缺失项。

    参数说明：
        base_dir:
            cur 目录路径。

        d_fqn:
            Deprecated API 的目录名（即 split_cur_name 解析得到的左侧 fqn）。

        query_labels:
            query 版本标签列表（stem）。

    返回说明：
        (keep, misses)
    """
    keep: List[str] = []
    misses: List[str] = []
    query_dir = base_dir / d_fqn
    for q in query_labels:
        if (query_dir / f"{q}.py").is_file():
            keep.append(q)
        else:
            misses.append(q)
    return keep, misses


def validate_candidate_dirs(base_dir: Path, candidate_labels: List[str]) -> Tuple[List[str], List[str]]:
    """
    功能说明：
        校验 candidate 版本目录是否存在，并分离可用与缺失项。

    参数说明：
        base_dir:
            cur 目录路径。

        candidate_labels:
            candidate 版本标签列表（目录名）。

    返回说明：
        (keep, misses)
    """
    keep: List[str] = []
    misses: List[str] = []
    candidate_root = base_dir / "R_candidates"
    for c in candidate_labels:
        if (candidate_root / c).is_dir():
            keep.append(c)
        else:
            misses.append(c)
    return keep, misses


def generate_three_routes_jsons(prefix: str, cur: str, only_experiments: Set[str]) -> Tuple[List[Dict[str, str]], List[str], Dict[str, int]]:
    """
    功能说明：
        处理单个 cur，按 compare_versions.json 的 3 个实验配置生成结果 JSON。

    参数说明：
        prefix:
            prefix 目录路径字符串（root/libname）。

        cur:
            cur 目录名字符串（通常为 fqn_D-fqn_R）。

        only_experiments:
            仅运行的实验名集合。

    返回说明：
        (saved_files, error_lines, cur_stats)

        saved_files:
            生成的 JSON 文件信息列表。

        error_lines:
            5 段式错误行列表，格式：
            [cur名] | [api文件名/query名] | [算法] | [阶段] | [简短报错原因]

        cur_stats:
            query/candidate 的失败统计。
    """
    prefix_path = Path(prefix)
    cur_path = Path(cur)
    base_dir = prefix_path / cur_path

    log_file = base_dir / "run.log"
    logger = setup_logger(
        log_file,
        logger_name=f"similarity_rank_three_routes_logger::{base_dir}",
        enable_console=False,
        file_mode="a",
    )

    logger.info("开始处理")
    logger.info("prefix: %s", prefix_path)
    logger.info("cur: %s", cur_path)
    logger.info("base_dir: %s", base_dir)

    cur_name = cur_path.name
    d_fqn, _ = split_cur_name(cur_name)

    compare_file = base_dir / "compare_versions.json"
    plan, plan_error = load_compare_plan(compare_file)
    if plan_error is not None:
        logger.error("compare_versions.json 读取失败：%s", plan_error)
        return [], [], {
            "query_failed_count": 0,
            "query_total_count": 0,
            "candidate_failed_count": 0,
            "candidate_total_count": 0,
        }

    algorithm_names: List[str] = ["tokenBased", "treeBased", "mapBased"]

    saved_files: List[Dict[str, str]] = []
    all_error_lines: List[str] = []
    failed_query_labels: Set[str] = set()
    failed_candidate_keys: Set[str] = set()

    for exp_name in ["fix_D", "fix_D_t", "fix_R"]:
        if exp_name not in only_experiments:
            continue

        spec = extract_experiment_spec(plan, exp_name)
        if not spec.get("enabled", False):
            logger.info("跳过实验：experiment=%s, enabled=false, reason=%s", exp_name, spec.get("reason", ""))
            continue

        query_labels, candidate_labels = resolve_versions_for_experiment(exp_name, spec)

        query_labels, missing_queries = validate_query_files(base_dir, d_fqn, query_labels)
        candidate_labels, missing_candidates = validate_candidate_dirs(base_dir, candidate_labels)

        if missing_queries:
            logger.warning("实验版本缺失，queries 跳过缺失项：experiment=%s, missing_queries=%s", exp_name, ",".join(missing_queries))
        if missing_candidates:
            logger.warning(
                "实验版本缺失，candidates 跳过缺失项：experiment=%s, missing_candidates=%s",
                exp_name,
                ",".join(missing_candidates),
            )

        if not query_labels:
            logger.info("跳过实验：experiment=%s, reason=no usable queries", exp_name)
            continue
        if not candidate_labels:
            logger.info("跳过实验：experiment=%s, reason=no usable candidates", exp_name)
            continue

        query_dir = base_dir / d_fqn
        query_code_map: Dict[str, str] = {}
        for q in query_labels:
            q_file = query_dir / f"{q}.py"
            try:
                code = read_text_file(q_file)
            except Exception as e:
                clean_error_msg = str(e).replace("\n", " ").replace("\r", "")
                error_line = f"{cur_name} | {q} | - | query_read | {clean_error_msg}"
                all_error_lines.append(error_line)
                continue
            if not code.strip():
                logger.warning("查询版本内容为空，已跳过：experiment=%s, query=%s, file=%s", exp_name, q, q_file)
                continue
            query_code_map[q] = code

        if not query_code_map:
            logger.info("跳过实验：experiment=%s, reason=all queries empty/unreadable", exp_name)
            continue

        candidate_root = base_dir / "R_candidates"
        candidate_dir_map: Dict[str, Path] = {c: (candidate_root / c) for c in candidate_labels}

        for algorithm_name in algorithm_names:
            logger.info("========================================")
            logger.info("开始处理：experiment=%s, algorithm=%s", exp_name, algorithm_name)
            logger.info("========================================")

            compiled_query_map, query_error_lines = compile_query_representations(
                query_code_map=query_code_map,
                algorithm_name=algorithm_name,
                cur_name=cur_name,
                logger=logger,
            )
            all_error_lines.extend(query_error_lines)
            for line in query_error_lines:
                parts = line.split(" | ", 4)
                if len(parts) >= 4 and parts[3] == "query_build":
                    failed_query_labels.add(parts[1])

            if not compiled_query_map:
                logger.warning("当前算法下所有 query 编译失败，跳过：experiment=%s, algorithm=%s", exp_name, algorithm_name)
                continue

            try:
                for candidate_label, target_candidate_dir in candidate_dir_map.items():
                    active_compiled_queries = dict(compiled_query_map)

                    logger.info(
                        "开始处理 candidate 版本：experiment=%s, algorithm=%s, candidate=%s, query_count=%d",
                        exp_name,
                        algorithm_name,
                        candidate_label,
                        len(active_compiled_queries),
                    )

                    unsorted_result_map, batch_error_lines = rank_candidates_by_similarity(
                        compiled_queries=active_compiled_queries,
                        candidate_dir=target_candidate_dir,
                        algorithm_name=algorithm_name,
                        cur_name=cur_name,
                        logger=logger,
                    )
                    all_error_lines.extend(batch_error_lines)
                    for line in batch_error_lines:
                        parts = line.split(" | ", 4)
                        if len(parts) >= 4 and parts[3] != "query_build":
                            failed_candidate_keys.add(f"{candidate_label}/{parts[1]}")

                    for q_label, unsorted_results in unsorted_result_map.items():
                        ranked_result = finalize_ranked_results(unsorted_results)

                        output_dir = base_dir / "result" / exp_name / f"{q_label}-{candidate_label}"
                        output_dir.mkdir(parents=True, exist_ok=True)

                        output_file = output_dir / f"{algorithm_name}.json"
                        output_file.write_text(
                            json.dumps(ranked_result, ensure_ascii=False, indent=2),
                            encoding="utf-8",
                        )

                        saved_files.append(
                            {
                                "cur": cur_name,
                                "experiment": exp_name,
                                "query": q_label,
                                "candidate": candidate_label,
                                "algorithm": algorithm_name,
                                "output": str(output_file),
                            }
                        )
            finally:
                compiled_query_map.clear()

    query_total_count = len(plan.get("inputs", {}).get("D_has_versions", [])) if isinstance(plan.get("inputs", {}), dict) else 0
    candidate_total_count = len(plan.get("inputs", {}).get("R_has_versions", [])) if isinstance(plan.get("inputs", {}), dict) else 0

    return saved_files, all_error_lines, {
        "query_failed_count": len(failed_query_labels),
        "query_total_count": query_total_count,
        "candidate_failed_count": len(failed_candidate_keys),
        "candidate_total_count": candidate_total_count,
    }


def process_one_cur(prefix: str, cur: str, only_experiments: Set[str]) -> Dict[str, Any]:
    """
    功能说明：
        封装单个 cur 的处理，捕获异常并返回结构化结果，供 main 汇总。

    参数说明：
        prefix:
            prefix 目录路径字符串。

        cur:
            cur 目录名字符串。

        only_experiments:
            仅运行的实验名集合。

    返回说明：
        包含 success/saved_files/error_lines/cur_stats 等字段的字典。
    """
    try:
        saved_files, error_lines, cur_stats = generate_three_routes_jsons(
            prefix=prefix,
            cur=cur,
            only_experiments=only_experiments,
        )
        return {
            "prefix": prefix,
            "cur": cur,
            "success": True,
            "saved_files": saved_files,
            "error_lines": error_lines,
            "cur_stats": cur_stats,
            "error": None,
            "traceback": None,
        }
    except Exception as e:
        return {
            "prefix": prefix,
            "cur": cur,
            "success": False,
            "saved_files": [],
            "error_lines": [],
            "cur_stats": {
                "query_failed_count": 0,
                "query_total_count": 0,
                "candidate_failed_count": 0,
                "candidate_total_count": 0,
            },
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


def main() -> None:
    """
    功能说明：
        脚本主入口：
        - 遍历 root 下所有 prefix/libname 与其下所有 cur
        - 每个 cur 读取 compare_versions.json 按实验配置生成结果
        - main 日志与错误日志写入 /media/he/Rbench/similarity 下

    参数说明：
        root:
            待处理 root 目录路径。

        overwrite:
            main 日志存在时是否覆盖继续执行。

        only_experiments:
            仅运行指定实验，逗号分隔：fix_D,fix_D_t,fix_R。

        candidates_workers:
            覆盖 rank.CANDIDATES_WORKERS（0=自动，>0=并发上限）。

        rank_worker_max_tasks:
            覆盖 rank.RANK_WORKER_MAX_TASKS（candidate 子进程最大复用任务数）。
    """
    parser = argparse.ArgumentParser(description="Rank Similarity for Three Routes Experiments")
    parser.add_argument("root", type=str, help="待处理的 root 目录路径")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="当 main 日志文件已存在时，继续执行并覆盖该日志文件",
    )
    parser.add_argument(
        "--only-experiments",
        type=str,
        default=None,
        help="仅运行指定实验，逗号分隔：fix_D,fix_D_t,fix_R",
    )
    parser.add_argument(
        "--candidates-workers",
        type=int,
        default=None,
        help="覆盖 rank.CANDIDATES_WORKERS（0=自动，>0=并发上限）",
    )
    parser.add_argument(
        "--rank-worker-max-tasks",
        type=int,
        default=None,
        help="覆盖 rank.RANK_WORKER_MAX_TASKS（candidate 子进程最大复用任务数）",
    )
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    root_path = Path(args.root).resolve()
    if not root_path.is_dir():
        raise FileNotFoundError(f"root 目录不存在：{root_path}")

    if args.candidates_workers is not None:
        global CANDIDATES_WORKERS
        CANDIDATES_WORKERS = int(args.candidates_workers)
    if args.rank_worker_max_tasks is not None:
        global RANK_WORKER_MAX_TASKS
        RANK_WORKER_MAX_TASKS = int(args.rank_worker_max_tasks)

    try:
        rel_path = root_path.relative_to(base_dir)
        log_name_stem = str(rel_path).replace("/", "_").replace("\\", "_")
    except ValueError:
        log_name_stem = str(root_path).replace("/", "_").replace("\\", "_").strip("_")

    if not log_name_stem or log_name_stem == ".":
        log_name_stem = "root"

    root_log_file = base_dir / f"rank_three_routes_main_{log_name_stem}.log"

    error_dir = base_dir / "run_error"
    error_dir.mkdir(parents=True, exist_ok=True)
    error_log_file = error_dir / f"error_candidates_three_routes_{log_name_stem}.log"

    if root_log_file.exists() and (not args.overwrite):
        print(f"main 日志已存在，未传 --overwrite，脚本退出：{root_log_file}")
        return

    if error_log_file.exists():
        error_log_file.write_text("")

    main_logger = setup_logger(
        root_log_file,
        logger_name=f"similarity_rank_three_routes_main::{root_path}",
        enable_console=False,
        file_mode="w",
    )

    only_experiments = normalize_experiment_names(args.only_experiments)

    prefix_dirs = sorted([p for p in root_path.iterdir() if p.is_dir()], key=lambda p: p.name)
    cur_tasks: List[Tuple[int, str, str]] = []
    task_seq = 0
    prefix_count = 0

    for prefix_dir in prefix_dirs:
        prefix_count += 1
        subdirs = sorted([p for p in prefix_dir.iterdir() if p.is_dir()], key=lambda p: p.name)
        for subdir in subdirs:
            task_seq += 1
            cur_tasks.append((task_seq, str(prefix_dir), subdir.name))

    main_logger.info("开始处理 root: %s", root_path)
    main_logger.info("共发现 %d 个 prefix 目录", prefix_count)
    main_logger.info("共发现 %d 个 cur 任务", len(cur_tasks))
    main_logger.info("仅运行实验集合：%s", ",".join(sorted(only_experiments)))

    if not cur_tasks:
        main_logger.info("没有可处理的 cur 任务")
        return

    all_saved_files: List[Dict[str, str]] = []
    success_count = 0
    failed_count = 0
    total_error_candidates = 0
    total_query_compile_failed = 0

    for seq, prefix, cur in cur_tasks:
        cur_start_time = time.perf_counter()
        result = process_one_cur(prefix=prefix, cur=cur, only_experiments=only_experiments)
        result["seq"] = seq
        cur_elapsed_seconds = time.perf_counter() - cur_start_time

        error_lines = result.get("error_lines", [])
        cur_stats = result.get("cur_stats", {})
        cur_query_build_failed_count = int(cur_stats.get("query_failed_count", 0))
        cur_query_total_count = int(cur_stats.get("query_total_count", 0))
        cur_candidate_failed_count = int(cur_stats.get("candidate_failed_count", 0))
        cur_candidate_total_count = int(cur_stats.get("candidate_total_count", 0))

        if error_lines:
            total_error_candidates += len(error_lines)
            total_query_compile_failed += cur_query_build_failed_count
            with error_log_file.open("a", encoding="utf-8") as f:
                for line in error_lines:
                    f.write(line + "\n")

        if result["success"]:
            saved_files = result.get("saved_files", [])
            all_saved_files.extend(saved_files)
            success_count += 1
            main_logger.info(
                "[%d/%d] cur 处理完成: prefix=%s, cur=%s，生成 %d 个结果文件，query失败数：%d/%d，candidate失败数：%d/%d，耗时=%.3f秒",
                seq,
                len(cur_tasks),
                prefix,
                cur,
                len(saved_files),
                cur_query_build_failed_count,
                cur_query_total_count,
                cur_candidate_failed_count,
                cur_candidate_total_count,
                cur_elapsed_seconds,
            )
        else:
            failed_count += 1
            main_logger.error(
                "[%d/%d] cur 处理失败: prefix=%s, cur=%s，错误: %s，query失败数：%d/%d，candidate失败数：%d/%d，耗时=%.3f秒",
                seq,
                len(cur_tasks),
                prefix,
                cur,
                result.get("error"),
                cur_query_build_failed_count,
                cur_query_total_count,
                cur_candidate_failed_count,
                cur_candidate_total_count,
                cur_elapsed_seconds,
            )
            if result.get("traceback"):
                main_logger.error("失败堆栈信息:\n%s", result["traceback"])

    main_logger.info("全部批量处理完成")
    main_logger.info("成功 cur 数: %d", success_count)
    main_logger.info("失败 cur 数: %d", failed_count)
    main_logger.info("总结果文件数: %d", len(all_saved_files))
    main_logger.info("query 编译总失败数: %d", total_query_compile_failed)
    main_logger.info("异常 Candidate 总数: %d，详情见: %s", total_error_candidates, error_log_file)


if __name__ == "__main__":
    main()
