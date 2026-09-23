# Diff 分块分析：py-polars.polars.series.series.Series.set_at_idx-py-polars.polars.series.series.Series.scatter-py-0.19.13
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.series.Series.set_at_idx-py-polars.polars.series.series.Series.scatter-py-0.19.13/py-polars.polars.series.series.Series.set_at_idx/Vi-1_py-0.19.13.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.series.Series.set_at_idx-py-polars.polars.series.series.Series.scatter-py-0.19.13/py-polars.polars.series.series.Series.set_at_idx/Vi_py-0.19.14.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.series.Series.set_at_idx-py-polars.polars.series.series.Series.scatter-py-0.19.13/R_candidates/py-1.0.0/py-polars.polars.series.series.Series.scatter.py
- 实验组：fix_R
- 总变更：+14 / -63 行
- 分块数：8

## Block 1 — block_001.patch
定位：@@ -1,1 +1,4 @@
说明：@deprecate_renamed_function("scatter", version="0.19.14")、@deprecate_renamed_parameter("idx", "indices", version="0.19、@deprecate_renamed_parameter("value", "values", version="0.1

## Block 2 — block_002.patch
定位：@@ -2,4 +5,4 @@
说明：idx: Series | np.ndarray[Any, Any] | Sequence[int] | int,、value: (、indices: Series | np.ndarray[Any, Any] | Sequence[int] | int...

## Block 3 — block_003.patch
定位：@@ -8,2 +11,4 @@
说明：| date、| datetime

## Block 4 — block_004.patch
定位：@@ -14,4 +19,2 @@
说明：| date、| datetime

## Block 5 — block_005.patch
定位：@@ -23,2 +26,5 @@
说明：.. deprecated:: 0.19.14、This method has been renamed to :meth:`scatter`.、

## Block 6 — block_006.patch
定位：@@ -25,3 +31,3 @@
说明：idx、indices

## Block 7 — block_007.patch
定位：@@ -27,44 +33,4 @@
说明：value、replacement values.、...

## Block 8 — block_008.patch
定位：@@ -70,17 +36,2 @@
说明：if isinstance(idx, int):、idx = [idx]、if len(idx) == 0:...
