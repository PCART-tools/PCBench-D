# Diff 分块分析：pandas.core.frame.DataFrame.clip_lower-pandas.core.generic.NDFrame.clip-v0.20.3
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.frame.DataFrame.clip_lower-pandas.core.generic.NDFrame.clip-v0.20.3/pandas.core.frame.DataFrame.clip_lower/Vi-1_v0.20.3.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.frame.DataFrame.clip_lower-pandas.core.generic.NDFrame.clip-v0.20.3/pandas.core.frame.DataFrame.clip_lower/Vi_v0.21.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/pandas.core.frame.DataFrame.clip_lower-pandas.core.generic.NDFrame.clip-v0.20.3/R_candidates/v1.0.0/pandas.core.generic.NDFrame.clip.py
- 实验组：fix_R
- 总变更：+6 / -9 行
- 分块数：3

## Block 1 — block_001.patch
定位：@@ -1,2 +1,2 @@
说明：def clip_lower(self, threshold, axis=None):、def clip_lower(self, threshold, axis=None, inplace=False):

## Block 2 — block_002.patch
定位：@@ -9,2 +9,5 @@
说明：inplace : boolean, default False、Whether to perform the operation in place on the data、.. versionadded:: 0.21.0

## Block 3 — block_003.patch
定位：@@ -18,9 +21,3 @@
说明：if np.any(isnull(threshold)):、raise ValueError("Cannot use an NA value as a clip threshold、...
