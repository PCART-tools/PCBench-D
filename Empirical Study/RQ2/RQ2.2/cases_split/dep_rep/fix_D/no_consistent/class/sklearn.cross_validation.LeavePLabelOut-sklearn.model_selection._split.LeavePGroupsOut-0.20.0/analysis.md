# 一、突变情况分析

- **Total**: 40
- **替代API**: `sklearn.model_selection._split.LeavePGroupsOut`
- **10% 阈值**: 4.0

## Vi-1 (0.17.1-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 18 | 0.2396 |
| tokenBased | 2 | 0.5156 |

## Vi (0.17.1-0.20.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 3 | 0.3232 |
| tokenBased | 2 | 0.5145 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 18 | 3 | +15 | true |
| tokenBased | 2 | 2 | +0 | false |

```json
{
  "total": 40,
  "replacement_api": "sklearn.model_selection._split.LeavePGroupsOut",
  "threshold_10pct": 4.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 18,
      "score": 0.239641
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.515556
    }
  },
  "vi": {
    "mapBased": {
      "rank": 3,
      "score": 0.323168
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.514523
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 18,
      "vi_rank": 3,
      "delta": 15,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 2,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.LeavePGroupsOut.py`
- **new**: `R_candidates/Vi_0.20.1/sklearn.model_selection._split.LeavePGroupsOut.py`
- **+4 / -0**

```diff
--- R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.LeavePGroupsOut.py
+++ R_candidates/Vi_0.20.1/sklearn.model_selection._split.LeavePGroupsOut.py
@@ -28,3 +28,7 @@
             raise ValueError("The 'groups' parameter should not be None.")
         groups = check_array(groups, ensure_2d=False, dtype=None)
         return int(comb(len(np.unique(groups)), self.n_groups, exact=True))
+
+    def split(self, X, y=None, groups=None):
+        
+        return super(LeavePGroupsOut, self).split(X, y, groups)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.LeavePGroupsOut.py",
  "new_file": "R_candidates/Vi_0.20.1/sklearn.model_selection._split.LeavePGroupsOut.py",
  "lines_added": 4,
  "lines_removed": 0
}
```
