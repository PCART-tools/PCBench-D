# Diff 分块分析：pandas.core.dtypes.common.is_categorical-pandas.core.dtypes.common.is_categorical_dtype-v1.4.4
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/function/pandas.core.dtypes.common.is_categorical-pandas.core.dtypes.common.is_categorical_dtype-v1.4.4/pandas.core.dtypes.common.is_categorical/Vi-1_v1.4.4.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/function/pandas.core.dtypes.common.is_categorical-pandas.core.dtypes.common.is_categorical_dtype-v1.4.4/pandas.core.dtypes.common.is_categorical/Vi_v1.5.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/function/pandas.core.dtypes.common.is_categorical-pandas.core.dtypes.common.is_categorical_dtype-v1.4.4/R_candidates/v2.0.0/pandas.core.dtypes.common.is_categorical_dtype.py
- 实验组：fix_R
- 总变更：+4 / -1 行
- 分块数：2

## Block 1 — block_001.patch
定位：@@ -3,2 +3,5 @@
说明：、.. deprecated:: 1.1.0、Use ``is_categorical_dtype`` instead.

## Block 2 — block_002.patch
定位：@@ -33,3 +36,3 @@
说明：stacklevel=find_stack_level(),、stacklevel=find_stack_level(inspect.currentframe()),
