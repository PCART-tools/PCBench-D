# 一、突变情况分析

- **Total**: 40
- **替代API**: `sklearn.model_selection._split.GroupKFold`
- **10% 阈值**: 4.0

## Vi-1 (0.17.1-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 27 | 0.1327 |
| tokenBased | 1 | 0.7387 |

## Vi (0.17.1-0.20.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 20 | 0.2174 |
| tokenBased | 1 | 0.7155 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 27 | 20 | +7 | true |
| tokenBased | 1 | 1 | +0 | false |

```json
{
  "total": 40,
  "replacement_api": "sklearn.model_selection._split.GroupKFold",
  "threshold_10pct": 4.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 27,
      "score": 0.132675
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.738739
    }
  },
  "vi": {
    "mapBased": {
      "rank": 20,
      "score": 0.217406
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.715481
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 27,
      "vi_rank": 20,
      "delta": 7,
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

- **old**: `R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.GroupKFold.py`
- **new**: `R_candidates/Vi_0.20.1/sklearn.model_selection._split.GroupKFold.py`
- **+4 / -0**

```diff
--- R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.GroupKFold.py
+++ R_candidates/Vi_0.20.1/sklearn.model_selection._split.GroupKFold.py
@@ -43,3 +43,7 @@
 
         for f in range(self.n_splits):
             yield np.where(indices == f)[0]
+
+    def split(self, X, y=None, groups=None):
+        
+        return super(GroupKFold, self).split(X, y, groups)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.20.0/sklearn.model_selection._split.GroupKFold.py",
  "new_file": "R_candidates/Vi_0.20.1/sklearn.model_selection._split.GroupKFold.py",
  "lines_added": 4,
  "lines_removed": 0
}
```
