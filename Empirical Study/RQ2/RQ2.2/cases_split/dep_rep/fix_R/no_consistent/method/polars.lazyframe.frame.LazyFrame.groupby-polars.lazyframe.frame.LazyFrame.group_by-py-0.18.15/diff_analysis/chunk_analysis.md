# Diff 分块分析：py-polars.polars.lazyframe.frame.LazyFrame.groupby-py-polars.polars.lazyframe.frame.LazyFrame.group_by-py-0.18.15
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.groupby-py-polars.polars.lazyframe.frame.LazyFrame.group_by-py-0.18.15/py-polars.polars.lazyframe.frame.LazyFrame.groupby/Vi-1_py-0.18.15.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.groupby-py-polars.polars.lazyframe.frame.LazyFrame.group_by-py-0.18.15/py-polars.polars.lazyframe.frame.LazyFrame.groupby/Vi_py-0.19.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.groupby-py-polars.polars.lazyframe.frame.LazyFrame.group_by-py-0.18.15/R_candidates/py-1.0.0/py-polars.polars.lazyframe.frame.LazyFrame.group_by.py
- 实验组：fix_R
- 总变更：+7 / -76 行
- 分块数：5

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_renamed_function("group_by", version="0.19.0")

## Block 2 — block_002.patch
定位：@@ -7,3 +8,6 @@
说明：Start a groupby operation.、Start a group by operation.、...

## Block 3 — block_003.patch
定位：@@ -18,3 +22,3 @@
说明：This is slower than a default groupby.、This is slower than a default group by.

## Block 4 — block_004.patch
定位：@@ -22,73 +26,2 @@
说明：Examples、--------、Group by one column and call ``agg`` to compute the grouped ...

## Block 5 — block_005.patch
定位：@@ -94,4 +27,2 @@
说明：exprs = parse_as_list_of_expressions(by, *more_by)、lgb = self._ldf.groupby(exprs, maintain_order)、return LazyGroupBy(lgb)...
