# Diff 分块分析：pandas.core.frame.DataFrame.convert_objects-pandas.core.generic.NDFrame.convert_objects-v0.9.0
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.frame.DataFrame.convert_objects-pandas.core.generic.NDFrame.convert_objects-v0.9.0/pandas.core.frame.DataFrame.convert_objects/Vi-1_v0.9.0.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.frame.DataFrame.convert_objects-pandas.core.generic.NDFrame.convert_objects-v0.9.0/pandas.core.frame.DataFrame.convert_objects/Vi_v0.9.1.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.frame.DataFrame.convert_objects-pandas.core.generic.NDFrame.convert_objects-v0.9.0/R_candidates/v0.13.0/pandas.core.generic.NDFrame.convert_objects.py
- 实验组：fix_R
- 总变更：+2 / -1 行
- 分块数：2

## Block 1 — block_001.patch
定位：@@ -10,2 +10,3 @@
说明：convert_f = lambda x: lib.maybe_convert_objects(x, convert_d

## Block 2 — block_002.patch
定位：@@ -14,3 +15,3 @@
说明：new_data[col] = lib.maybe_convert_objects(s)、new_data[col] = convert_f(s)
