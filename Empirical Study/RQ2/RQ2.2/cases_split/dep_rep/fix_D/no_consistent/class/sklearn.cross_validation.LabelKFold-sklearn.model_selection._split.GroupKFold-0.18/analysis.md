# 一、突变情况分析

- **Total**: 33
- **替代API**: `sklearn.model_selection._split.GroupKFold`
- **10% 阈值**: 3.3

## Vi-1 (0.17.1-0.18)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 20 | 0.1606 |
| tokenBased | 1 | 0.7805 |

## Vi (0.17.1-0.18.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 25 | 0.1469 |
| tokenBased | 1 | 0.7678 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 20 | 25 | -5 | true |
| tokenBased | 1 | 1 | +0 | false |

```json
{
  "total": 33,
  "replacement_api": "sklearn.model_selection._split.GroupKFold",
  "threshold_10pct": 3.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 20,
      "score": 0.160626
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.780488
    }
  },
  "vi": {
    "mapBased": {
      "rank": 25,
      "score": 0.146934
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.767773
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 20,
      "vi_rank": 25,
      "delta": -5,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.18/sklearn.model_selection._split.GroupKFold.py`
- **new**: `R_candidates/Vi_0.18.1/sklearn.model_selection._split.GroupKFold.py`
- **+1 / -0**

```diff
--- R_candidates/Vi-1_0.18/sklearn.model_selection._split.GroupKFold.py
+++ R_candidates/Vi_0.18.1/sklearn.model_selection._split.GroupKFold.py
@@ -7,6 +7,7 @@
     def _iter_test_indices(self, X, y, groups):
         if groups is None:
             raise ValueError("The groups parameter should not be None")
+        groups = check_array(groups, ensure_2d=False, dtype=None)
 
         unique_groups, groups = np.unique(groups, return_inverse=True)
         n_groups = len(unique_groups)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.18/sklearn.model_selection._split.GroupKFold.py",
  "new_file": "R_candidates/Vi_0.18.1/sklearn.model_selection._split.GroupKFold.py",
  "lines_added": 1,
  "lines_removed": 0
}
```
