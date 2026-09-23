# Diff 分块分析：py-polars.polars.series.series.Series.take-py-polars.polars.series.series.Series.gather-py-0.19.13
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.series.Series.take-py-polars.polars.series.series.Series.gather-py-0.19.13/py-polars.polars.series.series.Series.take/Vi-1_py-0.19.13.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.series.Series.take-py-polars.polars.series.series.Series.gather-py-0.19.13/py-polars.polars.series.series.Series.take/Vi_py-0.19.14.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.series.Series.take-py-polars.polars.series.series.Series.gather-py-0.19.13/R_candidates/py-1.0.0/py-polars.polars.series.series.Series.gather.py
- 实验组：fix_R
- 总变更：+5 / -12 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_renamed_function("gather", version="0.19.14")

## Block 2 — block_002.patch
定位：@@ -6,2 +7,5 @@
说明：.. deprecated:: 0.19.14、This method has been renamed to :meth:`gather`.、

## Block 3 — block_003.patch
定位：@@ -10,14 +14,2 @@
说明：、Examples、--------...

## Block 4 — block_004.patch
定位：@@ -23,1 +15,2 @@
说明：return self.gather(indices)
