# Diff 分块分析：pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.7.3
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.7.3/pandas.core.series.Series.fillna/Vi-1_v0.7.3.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.7.3/pandas.core.series.Series.fillna/Vi_v0.8.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.7.3/R_candidates/v0.13.0/pandas.core.generic.NDFrame.fillna.py
- 实验组：fix_R
- 总变更：+15 / -15 行
- 分块数：7

## Block 1 — block_001.patch
定位：@@ -1,2 +1,4 @@
说明：def fillna(self, value=None, method='pad', inplace=False):、、def fillna(self, value=None, method='pad', inplace=False,...

## Block 2 — block_002.patch
定位：@@ -16,2 +18,4 @@
说明：limit : int, default None、Maximum size gap to forward or backward fill

## Block 3 — block_003.patch
定位：@@ -25,4 +29,2 @@
说明：mask = isnull(self.values)、

## Block 4 — block_004.patch
定位：@@ -29,2 +31,3 @@
说明：mask = isnull(self.values)

## Block 5 — block_005.patch
定位：@@ -34,11 +37,3 @@
说明：method = com._clean_fill_method(method)、、# sadness. for Python 2.5 compatibility...

## Block 6 — block_006.patch
定位：@@ -45,3 +40,9 @@
说明：self.values[:] = self.values.take(indexer)、values = self.values、else:...

## Block 7 — block_007.patch
定位：@@ -48,4 +49,3 @@
说明：new_values = self.values.take(indexer)、result = Series(new_values, index=self.index, name=self.name、result = Series(values, index=self.index, name=self.name)
