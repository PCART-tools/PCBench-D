# Diff 分块分析：py-polars.polars.series.series.Series.take_every-py-polars.polars.series.series.Series.gather_every-py-0.19.13
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/candidates_cause/fix_R/no_consistent/method/py-polars.polars.series.series.Series.take_every-py-polars.polars.series.series.Series.gather_every-py-0.19.13/py-polars.polars.series.series.Series.take_every/Vi-1_py-0.19.13.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/candidates_cause/fix_R/no_consistent/method/py-polars.polars.series.series.Series.take_every-py-polars.polars.series.series.Series.gather_every-py-0.19.13/py-polars.polars.series.series.Series.take_every/Vi_py-0.19.14.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/candidates_cause/fix_R/no_consistent/method/py-polars.polars.series.series.Series.take_every-py-polars.polars.series.series.Series.gather_every-py-0.19.13/R_candidates/py-1.0.0/py-polars.polars.series.series.Series.gather_every.py
- 实验组：fix_R
- 总变更：+8 / -10 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_renamed_function("gather_every", version="0.19.14

## Block 2 — block_002.patch
定位：@@ -4,12 +5,4 @@
说明：Examples、--------、>>> s = pl.Series("a", [1, 2, 3, 4])...

## Block 3 — block_003.patch
定位：@@ -15,2 +8,6 @@
说明：Parameters、----------、n...

## Block 4 — block_004.patch
定位：@@ -16,1 +13,2 @@
说明：return self.gather_every(n)
