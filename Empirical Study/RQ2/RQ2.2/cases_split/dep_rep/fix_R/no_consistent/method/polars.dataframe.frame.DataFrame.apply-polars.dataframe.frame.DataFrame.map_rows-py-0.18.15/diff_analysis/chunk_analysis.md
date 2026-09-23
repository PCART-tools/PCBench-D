# Diff 分块分析：py-polars.polars.dataframe.frame.DataFrame.apply-py-polars.polars.dataframe.frame.DataFrame.map_rows-py-0.18.15
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.dataframe.frame.DataFrame.apply-py-polars.polars.dataframe.frame.DataFrame.map_rows-py-0.18.15/py-polars.polars.dataframe.frame.DataFrame.apply/Vi-1_py-0.18.15.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.dataframe.frame.DataFrame.apply-py-polars.polars.dataframe.frame.DataFrame.map_rows-py-0.18.15/py-polars.polars.dataframe.frame.DataFrame.apply/Vi_py-0.19.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/py-polars.polars.dataframe.frame.DataFrame.apply-py-polars.polars.dataframe.frame.DataFrame.map_rows-py-0.18.15/R_candidates/py-1.0.0/py-polars.polars.dataframe.frame.DataFrame.map_rows.py
- 实验组：fix_R
- 总变更：+4 / -80 行
- 分块数：4

## Block 1 — block_001.patch
定位：@@ -1,1 +1,2 @@
说明：@deprecate_renamed_function("map_rows", version="0.19.0")

## Block 2 — block_002.patch
定位：@@ -10,19 +11,4 @@
说明：.. warning::、This method is much slower than the native expressions API.、Only use it if you cannot implement your logic otherwise....

## Block 3 — block_003.patch
定位：@@ -38,56 +24,2 @@
说明：Notes、-----、* The frame-level ``apply`` cannot track column names (as th...

## Block 4 — block_004.patch
定位：@@ -93,10 +25,2 @@
说明：# TODO:、# from polars.utils.udfs import warn_on_inefficient_apply、# warn_on_inefficient_apply(function, columns=self.columns, ...
