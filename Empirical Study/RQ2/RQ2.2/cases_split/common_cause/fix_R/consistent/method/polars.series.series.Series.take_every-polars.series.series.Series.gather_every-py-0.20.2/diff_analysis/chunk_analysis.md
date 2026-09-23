# Diff 分块分析：py-polars.polars.series.series.Series.take_every-py-polars.polars.series.series.Series.gather_every-py-0.20.2
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.series.Series.take_every-py-polars.polars.series.series.Series.gather_every-py-0.20.2/py-polars.polars.series.series.Series.take_every/Vi-1_py-0.20.2.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.series.Series.take_every-py-polars.polars.series.series.Series.gather_every-py-0.20.2/py-polars.polars.series.series.Series.take_every/Vi_py-0.20.3.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.series.series.Series.take_every-py-polars.polars.series.series.Series.gather_every-py-0.20.2/R_candidates/py-1.0.0/py-polars.polars.series.series.Series.gather_every.py
- 实验组：fix_R
- 总变更：+4 / -2 行
- 分块数：3

## Block 1 — block_001.patch
定位：@@ -1,3 +1,3 @@
说明：def take_every(self, n: int) -> Series:、def take_every(self, n: int, offset: int = 0) -> Series:

## Block 2 — block_002.patch
定位：@@ -12,2 +12,4 @@
说明：offset、Starting index.

## Block 3 — block_003.patch
定位：@@ -13,2 +15,2 @@
说明：return self.gather_every(n)、return self.gather_every(n, offset)
