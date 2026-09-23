# 一、突变情况分析

- **Total**: 40
- **替代API**: `sklearn.model_selection._split.GroupShuffleSplit`
- **10% 阈值**: 4.0

## Vi-1 (0.17.1-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 21 | 0.1947 |
| tokenBased | 1 | 0.6286 |

## Vi (0.17.1-0.20.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 9 | 0.2778 |
| tokenBased | 1 | 0.6010 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 21 | 9 | +12 | true |
| tokenBased | 1 | 1 | +0 | false |

```json
{
  "total": 40,
  "replacement_api": "sklearn.model_selection._split.GroupShuffleSplit",
  "threshold_10pct": 4.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 21,
      "score": 0.194659
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.628571
    }
  },
  "vi": {
    "mapBased": {
      "rank": 9,
      "score": 0.277763
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.601036
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 21,
      "vi_rank": 9,
      "delta": 12,
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

- **old**: `R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.GroupShuffleSplit.py`
- **new**: `R_candidates/Vi_0.20.1/sklearn.model_selection._split.GroupShuffleSplit.py`
- **+4 / -0**

```diff
--- R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.GroupShuffleSplit.py
+++ R_candidates/Vi_0.20.1/sklearn.model_selection._split.GroupShuffleSplit.py
@@ -31,3 +31,7 @@
             test = np.flatnonzero(np.in1d(group_indices, group_test))
 
             yield train, test
+
+    def split(self, X, y=None, groups=None):
+        
+        return super(GroupShuffleSplit, self).split(X, y, groups)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.GroupShuffleSplit.py",
  "new_file": "R_candidates/Vi_0.20.1/sklearn.model_selection._split.GroupShuffleSplit.py",
  "lines_added": 4,
  "lines_removed": 0
}
```
