# 一、突变情况分析

- **Total**: 40
- **替代API**: `sklearn.model_selection._split.LeaveOneGroupOut`
- **10% 阈值**: 4.0

## Vi-1 (0.17.1-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 28 | 0.1389 |
| tokenBased | 3 | 0.3765 |

## Vi (0.17.1-0.20.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 20 | 0.2220 |
| tokenBased | 3 | 0.3876 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 28 | 20 | +8 | true |
| tokenBased | 3 | 3 | +0 | false |

```json
{
  "total": 40,
  "replacement_api": "sklearn.model_selection._split.LeaveOneGroupOut",
  "threshold_10pct": 4.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 28,
      "score": 0.138895
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.376543
    }
  },
  "vi": {
    "mapBased": {
      "rank": 20,
      "score": 0.221999
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.38764
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 28,
      "vi_rank": 20,
      "delta": 8,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 3,
      "vi_rank": 3,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.LeaveOneGroupOut.py`
- **new**: `R_candidates/Vi_0.20.1/sklearn.model_selection._split.LeaveOneGroupOut.py`
- **+4 / -0**

```diff
--- R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.LeaveOneGroupOut.py
+++ R_candidates/Vi_0.20.1/sklearn.model_selection._split.LeaveOneGroupOut.py
@@ -20,3 +20,7 @@
             raise ValueError("The 'groups' parameter should not be None.")
         groups = check_array(groups, ensure_2d=False, dtype=None)
         return len(np.unique(groups))
+
+    def split(self, X, y=None, groups=None):
+        
+        return super(LeaveOneGroupOut, self).split(X, y, groups)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.LeaveOneGroupOut.py",
  "new_file": "R_candidates/Vi_0.20.1/sklearn.model_selection._split.LeaveOneGroupOut.py",
  "lines_added": 4,
  "lines_removed": 0
}
```
