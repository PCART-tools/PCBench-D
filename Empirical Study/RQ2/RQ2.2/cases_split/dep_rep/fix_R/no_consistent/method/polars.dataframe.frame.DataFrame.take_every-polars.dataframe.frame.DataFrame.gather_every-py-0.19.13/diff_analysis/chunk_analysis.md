# Diff 分块分析：py-polars.polars.dataframe.frame.DataFrame.take_every-py-polars.polars.dataframe.frame.DataFrame.gather_every-py-0.19.13
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.dataframe.frame.DataFrame.take_every-py-polars.polars.dataframe.frame.DataFrame.gather_every-py-0.19.13/py-polars.polars.dataframe.frame.DataFrame.take_every/Vi-1_py-0.19.13.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.dataframe.frame.DataFrame.take_every-py-polars.polars.dataframe.frame.DataFrame.gather_every-py-0.19.13/py-polars.polars.dataframe.frame.DataFrame.take_every/Vi_py-0.19.14.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.dataframe.frame.DataFrame.take_every-py-polars.polars.dataframe.frame.DataFrame.gather_every-py-0.19.13/R_candidates/py-1.0.0/py-polars.polars.dataframe.frame.DataFrame.gather_every.py
- 实验组：fix_R
- 总变更：+8 / -14 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_renamed_function("gather_every", version="0.19.12

## Block 2 — block_002.patch
定位：@@ -4,15 +5,4 @@
说明：Examples、--------、>>> s = pl.DataFrame({"a": [1, 2, 3, 4], "b": [5, 6, 7, 8]})...

## Block 3 — block_003.patch
定位：@@ -18,2 +8,6 @@
说明：Parameters、----------、n...

## Block 4 — block_004.patch
定位：@@ -19,2 +13,2 @@
说明：return self.select(F.col("*").take_every(n))、return self.gather_every(n)
