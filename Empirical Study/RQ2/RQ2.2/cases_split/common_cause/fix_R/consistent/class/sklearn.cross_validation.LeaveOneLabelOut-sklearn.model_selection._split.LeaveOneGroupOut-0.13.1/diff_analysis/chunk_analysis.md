# Diff 分块分析：sklearn.cross_validation.LeaveOneLabelOut-sklearn.model_selection._split.LeaveOneGroupOut-0.13.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/class/sklearn.cross_validation.LeaveOneLabelOut-sklearn.model_selection._split.LeaveOneGroupOut-0.13.1/sklearn.cross_validation.LeaveOneLabelOut/Vi-1_0.13.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/class/sklearn.cross_validation.LeaveOneLabelOut-sklearn.model_selection._split.LeaveOneGroupOut-0.13.1/sklearn.cross_validation.LeaveOneLabelOut/Vi_0.14.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/class/sklearn.cross_validation.LeaveOneLabelOut-sklearn.model_selection._split.LeaveOneGroupOut-0.13.1/R_candidates/0.20.0/sklearn.model_selection._split.LeaveOneGroupOut.py
- 实验组：fix_R
- 总变更：+9 / -16 行
- 分块数：3

## Block 1 — block_001.patch
定位：@@ -1,2 +1,2 @@
说明：class LeaveOneLabelOut(object):、class LeaveOneLabelOut(_PartitionIterator):

## Block 2 — block_002.patch
定位：@@ -49,5 +49,7 @@
说明：self.labels = labels、self.n_unique_labels = unique(labels).size、self.indices = indices...

## Block 3 — block_003.patch
定位：@@ -53,14 +55,5 @@
说明：def __iter__(self):、# We make a copy here to avoid side-effects during iteration、labels = np.array(self.labels, copy=True)...
