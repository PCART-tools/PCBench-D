# 一、突变情况分析

- **Total**: 33
- **替代API**: `sklearn.model_selection._split.LeavePGroupsOut`
- **10% 阈值**: 3.3

## Vi-1 (0.17.1-0.18)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 12 | 0.2497 |
| tokenBased | 1 | 0.5657 |

## Vi (0.17.1-0.18.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 19 | 0.2306 |
| tokenBased | 2 | 0.5043 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 12 | 19 | -7 | true |
| tokenBased | 1 | 2 | -1 | false |

```json
{
  "total": 33,
  "replacement_api": "sklearn.model_selection._split.LeavePGroupsOut",
  "threshold_10pct": 3.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 12,
      "score": 0.249671
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.565657
    }
  },
  "vi": {
    "mapBased": {
      "rank": 19,
      "score": 0.230649
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.50431
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 12,
      "vi_rank": 19,
      "delta": -7,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.18/sklearn.model_selection._split.LeavePGroupsOut.py`
- **new**: `R_candidates/Vi_0.18.1/sklearn.model_selection._split.LeavePGroupsOut.py`
- **+9 / -1**

```diff
--- R_candidates/Vi-1_0.18/sklearn.model_selection._split.LeavePGroupsOut.py
+++ R_candidates/Vi_0.18.1/sklearn.model_selection._split.LeavePGroupsOut.py
@@ -7,8 +7,14 @@
     def _iter_test_masks(self, X, y, groups):
         if groups is None:
             raise ValueError("The groups parameter should not be None")
-        groups = np.array(groups, copy=True)
+        groups = check_array(groups, copy=True, ensure_2d=False, dtype=None)
         unique_groups = np.unique(groups)
+        if self.n_groups >= len(unique_groups):
+            raise ValueError(
+                "The groups parameter contains fewer than (or equal to) "
+                "n_groups (%d) numbers of unique groups (%s). LeavePGroupsOut "
+                "expects that at least n_groups + 1 (%d) unique groups be "
+                "present" % (self.n_groups, unique_groups, self.n_groups + 1))
         combi = combinations(range(len(unique_groups)), self.n_groups)
         for indices in combi:
             test_index = np.zeros(_num_samples(X), dtype=np.bool)
@@ -20,4 +26,6 @@
         
         if groups is None:
             raise ValueError("The groups parameter should not be None")
+        groups = check_array(groups, ensure_2d=False, dtype=None)
+        X, y, groups = indexable(X, y, groups)
         return int(comb(len(np.unique(groups)), self.n_groups, exact=True))
```

```json
{
  "old_file": "R_candidates/Vi-1_0.18/sklearn.model_selection._split.LeavePGroupsOut.py",
  "new_file": "R_candidates/Vi_0.18.1/sklearn.model_selection._split.LeavePGroupsOut.py",
  "lines_added": 9,
  "lines_removed": 1
}
```
