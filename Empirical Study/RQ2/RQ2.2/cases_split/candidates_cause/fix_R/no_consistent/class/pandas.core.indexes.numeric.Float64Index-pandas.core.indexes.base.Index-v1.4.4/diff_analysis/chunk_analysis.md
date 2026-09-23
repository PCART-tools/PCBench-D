# Diff 分块分析：pandas.core.indexes.numeric.Float64Index-pandas.core.indexes.base.Index-v1.4.4
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/class/pandas.core.indexes.numeric.Float64Index-pandas.core.indexes.base.Index-v1.4.4/pandas.core.indexes.numeric.Float64Index/Vi-1_v1.4.4.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/class/pandas.core.indexes.numeric.Float64Index-pandas.core.indexes.base.Index-v1.4.4/pandas.core.indexes.numeric.Float64Index/Vi_v1.5.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/class/pandas.core.indexes.numeric.Float64Index-pandas.core.indexes.base.Index-v1.4.4/R_candidates/v2.0.0/pandas.core.indexes.base.Index.py
- 实验组：fix_R
- 总变更：+4 / -1 行
- 分块数：2

## Block 1 — block_001.patch
定位：@@ -10,3 +10,2 @@
说明：_engine_type = libindex.Float64Engine

## Block 2 — block_002.patch
定位：@@ -14,1 +13,5 @@
说明：、@property、def _engine_type(self) -> type[libindex.Float64Engine]:...
