#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计源码定义过渡阶段与调用过渡阶段的数量（含粒度细分）。

读取同目录下的 final_dataset.xlsx（即 deprecated_api_replacement_api_mappings.xlsx 的副本），
按字符串比较弃用声明版本(A)、源码删除版本(G)、调用失效版本(H)，输出两个过渡阶段的总数
以及 class/function/method 各粒度的数量。
"""
from pathlib import Path
import pandas as pd

X = Path(__file__).resolve().parent / "final_dataset.xlsx"

GRANULARITIES = ["class", "function", "method"]

# ---------------------------------------------------------------------------
# 人工确认的版本记录异常 case 清单。
#
# 以下 21 个 case 的 removal_version / actual_invalid_version 早于
# documented_deprecation_version，属于版本记录口径不一致（日志或收集口径问题），
# 而非真实的过渡阶段，需从对应过渡阶段计数中扣除。
#
# 扣除口径：
#   source — 源码删除版本(G)早于弃用声明版本(A)，仅从源码过渡阶段计数中扣除；
#   both   — 源码删除版本(G)与调用失效版本(H)均早于弃用声明版本(A)，
#            两个过渡阶段计数各扣除 1。
#
# 各粒度的扣除数量由此清单汇总得到（见下方两个常量），脚本直接按粒度扣除，
# 无需与 xlsx 中的行逐一匹配。
#
# class（source × 1）：
#   jax.interpreters.pxla.Mesh                                          — source
# function（source × 3）：
#   pandas.tools.plotting.scatter_matrix                                — source
#   jax._src.core.has_opaque_dtype                                      — source
#   jax._src.dtypes.is_opaque_dtype                                     — source
# method（both × 17）：
#   pandas.core.generic.NDFrame.iterkv                                  — both
#   transformers.tokenization_roberta.RobertaTokenizer.add_special_tokens_sequence_pair   — both
#   transformers.tokenization_xlm.XLMTokenizer.add_special_tokens_sequence_pair           — both
#   transformers.tokenization_utils.PreTrainedTokenizer.add_special_tokens_sequence_pair  — both
#   transformers.tokenization_bert.BertTokenizer.add_special_tokens_sequence_pair         — both
#   transformers.tokenization_xlnet.XLNetTokenizer.add_special_tokens_sequence_pair       — both
#   transformers.tokenization_roberta.RobertaTokenizer.add_special_tokens_single_sequence — both
#   transformers.tokenization_xlm.XLMTokenizer.add_special_tokens_single_sequence         — both
#   transformers.tokenization_utils.PreTrainedTokenizer.add_special_tokens_single_sequence — both
#   transformers.tokenization_bert.BertTokenizer.add_special_tokens_single_sequence        — both
#   transformers.tokenization_xlnet.XLNetTokenizer.add_special_tokens_single_sequence      — both
#   transformers.trainer.Trainer._log                                    — both
#   transformers.trainer.Trainer._prediction_loop                        — both
#   transformers.trainer_tf.TFTrainer._prediction_loop                   — both
#   transformers.trainer_tf.TFTrainer._run_model                         — both
#   transformers.trainer_tf.TFTrainer._setup_wandb                       — both
#   transformers.trainer.Trainer._training_step                          — both
# ---------------------------------------------------------------------------

# 实际确认：源码删除版本早于弃用声明版本的数量（按粒度）
CONFIRMED_REMOVAL_BEFORE_ANNOUNCEMENT = {"class": 1, "function": 3, "method": 17}
# 实际确认：调用失效版本早于弃用声明版本的数量（按粒度）
CONFIRMED_INVALID_BEFORE_ANNOUNCEMENT = {"class": 0, "function": 0, "method": 17}


def norm_version(v):
    # 统一日志记录的版本号与 pypi 版本号格式：去掉末尾连续的 ".0" 后缀
    if v is None or pd.isna(v):
        return ""
    s = str(v).strip()
    if s == "":
        return ""
    while s.endswith(".0"):
        s = s[:-2]
    return s


xl = pd.ExcelFile(X)
a_neq_g = {g: 0 for g in GRANULARITIES}
a_neq_h = {g: 0 for g in GRANULARITIES}
for sheet in xl.sheet_names:
    df = pd.read_excel(X, sheet_name=sheet, header=0, dtype=str, keep_default_na=False)
    for _, r in df.iterrows():
        gran = r["granularity"]
        a = norm_version(r["documented_deprecation_version"])
        g = norm_version(r["removal_version"])
        h = norm_version(r["actual_invalid_version"])
        if a != g:
            a_neq_g[gran] += 1
        if a != h:
            a_neq_h[gran] += 1

source_transition = {
    g: a_neq_g[g] - CONFIRMED_REMOVAL_BEFORE_ANNOUNCEMENT[g]
    for g in GRANULARITIES
}
invocation_transition = {
    g: a_neq_h[g] - CONFIRMED_INVALID_BEFORE_ANNOUNCEMENT[g]
    for g in GRANULARITIES
}

print("source-definition transition period:")
for g in GRANULARITIES:
    print(f"  {g:<8}: {source_transition[g]}")
print(f"  {'total':<8}: {sum(source_transition.values())}")

print("original-invocation transition period:")
for g in GRANULARITIES:
    print(f"  {g:<8}: {invocation_transition[g]}")
print(f"  {'total':<8}: {sum(invocation_transition.values())}")
