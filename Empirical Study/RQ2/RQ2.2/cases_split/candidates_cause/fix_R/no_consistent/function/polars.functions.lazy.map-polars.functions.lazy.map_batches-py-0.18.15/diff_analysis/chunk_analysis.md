# Diff 分块分析：py-polars.polars.functions.lazy.map-py-polars.polars.functions.lazy.map_batches-py-0.18.15
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/py-polars.polars.functions.lazy.map-py-polars.polars.functions.lazy.map_batches-py-0.18.15/py-polars.polars.functions.lazy.map/Vi-1_py-0.18.15.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/py-polars.polars.functions.lazy.map-py-polars.polars.functions.lazy.map_batches-py-0.18.15/py-polars.polars.functions.lazy.map/Vi_py-0.19.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/py-polars.polars.functions.lazy.map-py-polars.polars.functions.lazy.map_batches-py-0.18.15/R_candidates/py-1.0.0/py-polars.polars.functions.lazy.map_batches.py
- 实验组：fix_R
- 总变更：+4 / -37 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_renamed_function("map_batches", version="0.19.0")

## Block 2 — block_002.patch
定位：@@ -8,3 +9,4 @@
说明：Produces a single Series result.、.. deprecated:: 0.19.0、This function has been renamed to :func:`map_batches`.

## Block 3 — block_003.patch
定位：@@ -24,32 +26,2 @@
说明：Examples、--------、>>> def test_func(a, b, c):...

## Block 4 — block_004.patch
定位：@@ -55,7 +27,2 @@
说明：exprs = parse_as_list_of_expressions(exprs)、return wrap_expr(、plr.map_mul(...
