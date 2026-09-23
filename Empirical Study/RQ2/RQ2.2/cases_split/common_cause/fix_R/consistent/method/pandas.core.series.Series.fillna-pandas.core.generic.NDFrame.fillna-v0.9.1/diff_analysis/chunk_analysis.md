# Diff 分块分析：pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.9.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.9.1/pandas.core.series.Series.fillna/Vi-1_v0.9.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.9.1/pandas.core.series.Series.fillna/Vi_v0.10.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.9.1/R_candidates/v0.13.0/pandas.core.generic.NDFrame.fillna.py
- 实验组：fix_R
- 总变更：+6 / -4 行
- 分块数：5

## Block 1 — block_001.patch
定位：@@ -1,3 +1,3 @@
说明：def fillna(self, value=None, method='pad', inplace=False,、def fillna(self, value=None, method=None, inplace=False,

## Block 2 — block_002.patch
定位：@@ -30,3 +30,3 @@
说明：return self.copy() if not inplace else self、return self.copy() if not inplace else None

## Block 3 — block_003.patch
定位：@@ -33,2 +33,4 @@
说明：if method is not None:、raise ValueError('Cannot specify both a fill value and metho

## Block 4 — block_004.patch
定位：@@ -38,3 +40,3 @@
说明：raise ValueError('must specify a fill method')、raise ValueError('must specify a fill method or value')

## Block 5 — block_005.patch
定位：@@ -54,2 +56,2 @@
说明：return result、return result if not inplace else None
