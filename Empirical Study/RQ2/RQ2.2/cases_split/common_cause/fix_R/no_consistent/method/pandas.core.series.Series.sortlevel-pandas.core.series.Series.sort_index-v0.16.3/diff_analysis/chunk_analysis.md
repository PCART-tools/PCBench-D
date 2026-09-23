# Diff 分块分析：pandas.core.series.Series.sortlevel-pandas.core.series.Series.sort_index-v0.16.3
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/method/pandas.core.series.Series.sortlevel-pandas.core.series.Series.sort_index-v0.16.3/pandas.core.series.Series.sortlevel/Vi-1_v0.16.3.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/method/pandas.core.series.Series.sortlevel-pandas.core.series.Series.sort_index-v0.16.3/pandas.core.series.Series.sortlevel/Vi_v0.17.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/no_consistent/method/pandas.core.series.Series.sortlevel-pandas.core.series.Series.sort_index-v0.16.3/R_candidates/v0.24.0/pandas.core.series.Series.sort_index.py
- 实验组：fix_R
- 总变更：+6 / -8 行
- 分块数：2

## Block 1 — block_001.patch
定位：@@ -14,2 +14,7 @@
说明：、See Also、--------...

## Block 2 — block_002.patch
定位：@@ -15,9 +20,2 @@
说明：if not isinstance(self.index, MultiIndex):、raise TypeError('can only sort by level with a hierarchical 、...
