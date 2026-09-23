# Diff 分块分析：pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.10.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.10.1/pandas.core.series.Series.fillna/Vi-1_v0.10.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.10.1/pandas.core.series.Series.fillna/Vi_v0.11.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.10.1/R_candidates/v0.13.0/pandas.core.generic.NDFrame.fillna.py
- 实验组：fix_R
- 总变更：+2 / -9 行
- 分块数：3

## Block 1 — block_001.patch
定位：@@ -29,7 +29,2 @@
说明：if inplace:、import warnings、warnings.warn("Series.fillna with inplace=True  will return ...

## Block 2 — block_002.patch
定位：@@ -35,3 +30,3 @@
说明：return self.copy() if not inplace else self、return self.copy() if not inplace else None

## Block 3 — block_003.patch
定位：@@ -61,5 +56,3 @@
说明：if inplace:、return self、else:...
