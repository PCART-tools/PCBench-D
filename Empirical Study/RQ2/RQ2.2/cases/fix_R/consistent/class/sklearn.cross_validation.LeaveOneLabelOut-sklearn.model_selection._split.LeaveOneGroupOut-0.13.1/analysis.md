# 一、突变情况分析

- **Total**: 40
- **替代API**: `sklearn.model_selection._split.LeaveOneGroupOut`
- **10% 阈值**: 4.0

## Vi-1 (0.13.1-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 33 | 0.1189 |
| tokenBased | 10 | 0.4098 |

## Vi (0.14-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 28 | 0.1390 |
| tokenBased | 3 | 0.3975 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 33 | 28 | +5 | true |
| tokenBased | 10 | 3 | +7 | true |

```json
{
  "total": 40,
  "replacement_api": "sklearn.model_selection._split.LeaveOneGroupOut",
  "threshold_10pct": 4.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 33,
      "score": 0.118936
    },
    "tokenBased": {
      "rank": 10,
      "score": 0.409836
    }
  },
  "vi": {
    "mapBased": {
      "rank": 28,
      "score": 0.139023
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.397516
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 33,
      "vi_rank": 28,
      "delta": 5,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 10,
      "vi_rank": 3,
      "delta": 7,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `sklearn.cross_validation.LeaveOneLabelOut/Vi-1_0.13.1.py`
- **new**: `sklearn.cross_validation.LeaveOneLabelOut/Vi_0.14.py`
- **+8 / -15**

```diff
--- sklearn.cross_validation.LeaveOneLabelOut/Vi-1_0.13.1.py
+++ sklearn.cross_validation.LeaveOneLabelOut/Vi_0.14.py
@@ -1,23 +1,16 @@
-class LeaveOneLabelOut(object):
+class LeaveOneLabelOut(_PartitionIterator):
     
 
     def __init__(self, labels, indices=True):
-        self.labels = labels
-        self.n_unique_labels = unique(labels).size
-        self.indices = indices
+        super(LeaveOneLabelOut, self).__init__(len(labels), indices)
 
-    def __iter__(self):
+        self.labels = np.array(labels, copy=True)
+        self.unique_labels = unique(labels)
+        self.n_unique_labels = len(self.unique_labels)
 
-        labels = np.array(self.labels, copy=True)
-        for i in unique(labels):
-            test_index = np.zeros(len(labels), dtype=np.bool)
-            test_index[labels == i] = True
-            train_index = np.logical_not(test_index)
-            if self.indices:
-                ind = np.arange(len(labels))
-                train_index = ind[train_index]
-                test_index = ind[test_index]
-            yield train_index, test_index
+    def _iter_test_masks(self):
+        for i in self.unique_labels:
+            yield self.labels == i
 
     def __repr__(self):
         return '%s.%s(labels=%s)' % (
```

```json
{
  "old_file": "sklearn.cross_validation.LeaveOneLabelOut/Vi-1_0.13.1.py",
  "new_file": "sklearn.cross_validation.LeaveOneLabelOut/Vi_0.14.py",
  "lines_added": 8,
  "lines_removed": 15
}
```
