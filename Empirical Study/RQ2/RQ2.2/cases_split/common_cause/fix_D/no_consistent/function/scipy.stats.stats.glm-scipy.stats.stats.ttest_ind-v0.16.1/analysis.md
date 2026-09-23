# 一、突变情况分析

- **Total**: 371
- **替代API**: `scipy.stats.stats.ttest_ind`
- **10% 阈值**: 37.1

## Vi-1 (v0.12.1-v0.16.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 57 | 0.4366 |
| tokenBased | 74 | 0.4375 |
| treeBased | 107 | 0.3946 |

## Vi (v0.12.1-v0.17.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 68 | 0.4209 |
| tokenBased | 21 | 0.5397 |
| treeBased | 54 | 0.4344 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 57 | 68 | -11 | false |
| tokenBased | 74 | 21 | +53 | true |
| treeBased | 107 | 54 | +53 | true |

```json
{
  "total": 371,
  "replacement_api": "scipy.stats.stats.ttest_ind",
  "threshold_10pct": 37.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 57,
      "score": 0.436622
    },
    "tokenBased": {
      "rank": 74,
      "score": 0.4375
    },
    "treeBased": {
      "rank": 107,
      "score": 0.394649
    }
  },
  "vi": {
    "mapBased": {
      "rank": 68,
      "score": 0.420883
    },
    "tokenBased": {
      "rank": 21,
      "score": 0.539749
    },
    "treeBased": {
      "rank": 54,
      "score": 0.434402
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 57,
      "vi_rank": 68,
      "delta": -11,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 74,
      "vi_rank": 21,
      "delta": 53,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 107,
      "vi_rank": 54,
      "delta": 53,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.16.1/scipy.stats.stats.ttest_ind.py`
- **new**: `R_candidates/Vi_v0.17.0/scipy.stats.stats.ttest_ind.py`
- **+10 / -1**

```diff
--- R_candidates/Vi-1_v0.16.1/scipy.stats.stats.ttest_ind.py
+++ R_candidates/Vi_v0.17.0/scipy.stats.stats.ttest_ind.py
@@ -1,6 +1,15 @@
-def ttest_ind(a, b, axis=0, equal_var=True):
+def ttest_ind(a, b, axis=0, equal_var=True, nan_policy='propagate'):
     
     a, b, axis = _chk2_asarray(a, b, axis)
+
+
+    contains_nan, nan_policy = (_contains_nan(a, nan_policy) or
+                                _contains_nan(b, nan_policy))
+
+    if contains_nan and nan_policy == 'omit':
+        a = ma.masked_invalid(a)
+        b = ma.masked_invalid(b)
+        return mstats_basic.ttest_ind(a, b, axis, equal_var)
 
     if a.size == 0 or b.size == 0:
         return Ttest_indResult(np.nan, np.nan)
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.16.1/scipy.stats.stats.ttest_ind.py",
  "new_file": "R_candidates/Vi_v0.17.0/scipy.stats.stats.ttest_ind.py",
  "lines_added": 10,
  "lines_removed": 1
}
```
