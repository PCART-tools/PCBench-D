# Diff 分块分析：pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.11.0
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.11.0/pandas.core.series.Series.fillna/Vi-1_v0.11.0.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.11.0/pandas.core.series.Series.fillna/Vi_v0.12.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.series.Series.fillna-pandas.core.generic.NDFrame.fillna-v0.11.0/R_candidates/v0.13.0/pandas.core.generic.NDFrame.fillna.py
- 实验组：fix_R
- 总变更：+3 / -0 行
- 分块数：1

## Block 1 — block_001.patch
定位：@@ -29,2 +29,5 @@
说明：if isinstance(value, (list, tuple)):、raise TypeError('"value" parameter must be a scalar or dict,、'you passed a "{0}"'.format(type(value).__name__))
