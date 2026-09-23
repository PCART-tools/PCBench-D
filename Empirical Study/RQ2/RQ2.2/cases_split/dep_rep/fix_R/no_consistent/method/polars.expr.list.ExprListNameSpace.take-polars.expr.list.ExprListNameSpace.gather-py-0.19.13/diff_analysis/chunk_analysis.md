# Diff 分块分析：py-polars.polars.expr.list.ExprListNameSpace.take-py-polars.polars.expr.list.ExprListNameSpace.gather-py-0.19.13
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.list.ExprListNameSpace.take-py-polars.polars.expr.list.ExprListNameSpace.gather-py-0.19.13/py-polars.polars.expr.list.ExprListNameSpace.take/Vi-1_py-0.19.13.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.list.ExprListNameSpace.take-py-polars.polars.expr.list.ExprListNameSpace.gather-py-0.19.13/py-polars.polars.expr.list.ExprListNameSpace.take/Vi_py-0.19.14.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.expr.list.ExprListNameSpace.take-py-polars.polars.expr.list.ExprListNameSpace.gather-py-0.19.13/R_candidates/py-1.0.0/py-polars.polars.expr.list.ExprListNameSpace.gather.py
- 实验组：fix_R
- 总变更：+5 / -7 行
- 分块数：5

## Block 1 — block_001.patch
定位：@@ -1,1 +1,3 @@
说明：@deprecate_renamed_function("gather", version="0.19.14")、@deprecate_renamed_parameter("index", "indices", version="0.

## Block 2 — block_002.patch
定位：@@ -2,3 +4,3 @@
说明：index: Expr | Series | list[int] | list[list[int]],、indices: Expr | Series | list[int] | list[list[int]],

## Block 3 — block_003.patch
定位：@@ -14,3 +16,3 @@
说明：index、indices

## Block 4 — block_004.patch
定位：@@ -21,3 +23,2 @@
说明：

## Block 5 — block_005.patch
定位：@@ -23,5 +24,2 @@
说明：if isinstance(index, list):、index = pl.Series(index)、index = parse_as_expression(index)...
