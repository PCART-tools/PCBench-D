# 一、突变情况分析

- **Total**: 382
- **替代API**: `scipy.stats.stats.ttest_ind`
- **10% 阈值**: 38.2

## Vi-1 (v0.12.1-v0.15.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 65 | 0.4214 |
| tokenBased | 18 | 0.5577 |
| treeBased | 34 | 0.4538 |

## Vi (v0.12.1-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 18 | 0.4931 |
| tokenBased | 68 | 0.4581 |
| treeBased | 79 | 0.4202 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 65 | 18 | +47 | true |
| tokenBased | 18 | 68 | -50 | true |
| treeBased | 34 | 79 | -45 | true |

```json
{
  "total": 382,
  "replacement_api": "scipy.stats.stats.ttest_ind",
  "threshold_10pct": 38.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 65,
      "score": 0.421394
    },
    "tokenBased": {
      "rank": 18,
      "score": 0.557692
    },
    "treeBased": {
      "rank": 34,
      "score": 0.453826
    }
  },
  "vi": {
    "mapBased": {
      "rank": 18,
      "score": 0.493085
    },
    "tokenBased": {
      "rank": 68,
      "score": 0.45815
    },
    "treeBased": {
      "rank": 79,
      "score": 0.420195
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 65,
      "vi_rank": 18,
      "delta": 47,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 18,
      "vi_rank": 68,
      "delta": -50,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 34,
      "vi_rank": 79,
      "delta": -45,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.15.1/scipy.stats.stats.ttest_ind.py`
- **new**: `R_candidates/Vi_v0.16.0/scipy.stats.stats.ttest_ind.py`
- **+9 / -17**

```diff
--- R_candidates/Vi-1_v0.15.1/scipy.stats.stats.ttest_ind.py
+++ R_candidates/Vi_v0.16.0/scipy.stats.stats.ttest_ind.py
@@ -1,30 +1,22 @@
 def ttest_ind(a, b, axis=0, equal_var=True):
     
     a, b, axis = _chk2_asarray(a, b, axis)
+
+    Ttest_indResult = namedtuple('Ttest_indResult', ('statistic', 'pvalue'))
+
     if a.size == 0 or b.size == 0:
-        return (np.nan, np.nan)
+        return Ttest_indResult(np.nan, np.nan)
 
     v1 = np.var(a, axis, ddof=1)
     v2 = np.var(b, axis, ddof=1)
     n1 = a.shape[axis]
     n2 = b.shape[axis]
 
-    if (equal_var):
-        df = n1 + n2 - 2
-        svar = ((n1 - 1) * v1 + (n2 - 1) * v2) / float(df)
-        denom = np.sqrt(svar * (1.0 / n1 + 1.0 / n2))
+    if equal_var:
+        df, denom = _equal_var_ttest_denom(v1, n1, v2, n2)
     else:
-        vn1 = v1 / n1
-        vn2 = v2 / n2
-        df = ((vn1 + vn2)**2) / ((vn1**2) / (n1 - 1) + (vn2**2) / (n2 - 1))
+        df, denom = _unequal_var_ttest_denom(v1, n1, v2, n2)
 
+    res = _ttest_ind_from_stats(np.mean(a, axis), np.mean(b, axis), denom, df)
 
-
-        df = np.where(np.isnan(df), 1, df)
-        denom = np.sqrt(vn1 + vn2)
-
-    d = np.mean(a, axis) - np.mean(b, axis)
-    t = np.divide(d, denom)
-    t, prob = _ttest_finish(df, t)
-
-    return t, prob
+    return Ttest_indResult(*res)
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.15.1/scipy.stats.stats.ttest_ind.py",
  "new_file": "R_candidates/Vi_v0.16.0/scipy.stats.stats.ttest_ind.py",
  "lines_added": 9,
  "lines_removed": 17
}
```
