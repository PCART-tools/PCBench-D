# Diff 分块分析：py-polars.polars.lazyframe.frame.LazyFrame.group_by_rolling-py-polars.polars.lazyframe.frame.LazyFrame.rolling-py-0.19.8
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.group_by_rolling-py-polars.polars.lazyframe.frame.LazyFrame.rolling-py-0.19.8/py-polars.polars.lazyframe.frame.LazyFrame.group_by_rolling/Vi-1_py-0.19.8.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.group_by_rolling-py-polars.polars.lazyframe.frame.LazyFrame.rolling-py-0.19.8/py-polars.polars.lazyframe.frame.LazyFrame.group_by_rolling/Vi_py-0.19.9.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.lazyframe.frame.LazyFrame.group_by_rolling-py-polars.polars.lazyframe.frame.LazyFrame.rolling-py-0.19.8/R_candidates/py-1.0.0/py-polars.polars.lazyframe.frame.LazyFrame.rolling.py
- 实验组：fix_R
- 总变更：+10 / -100 行
- 分块数：5

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_renamed_function("rolling", version="0.19.9")

## Block 2 — block_002.patch
定位：@@ -13,45 +14,4 @@
说明：Different from a ``dynamic_group_by`` the windows are now de、individual values and are not of constant intervals. For con、use :func:`LazyFrame.group_by_dynamic`....

## Block 3 — block_003.patch
定位：@@ -90,48 +50,2 @@
说明：See Also、--------、group_by_dynamic...

## Block 4 — block_004.patch
定位：@@ -137,12 +51,9 @@
说明：index_column = parse_as_expression(index_column)、if offset is None:、offset = _negate_duration(_timedelta_to_pl_duration(period))...

## Block 5 — block_005.patch
定位：@@ -148,2 +59,1 @@
说明：return LazyGroupBy(lgb)
