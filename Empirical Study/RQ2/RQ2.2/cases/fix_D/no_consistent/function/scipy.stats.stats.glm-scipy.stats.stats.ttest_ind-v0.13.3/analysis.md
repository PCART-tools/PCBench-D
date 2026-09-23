# 一、突变情况分析

- **Total**: 353
- **替代API**: `scipy.stats.stats.ttest_ind`
- **10% 阈值**: 35.3

## Vi-1 (v0.12.1-v0.13.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 112 | 0.3727 |
| tokenBased | 12 | 0.5685 |
| treeBased | 22 | 0.4639 |

## Vi (v0.12.1-v0.14.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 67 | 0.4214 |
| tokenBased | 18 | 0.5577 |
| treeBased | 31 | 0.4538 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 112 | 67 | +45 | true |
| tokenBased | 12 | 18 | -6 | false |
| treeBased | 22 | 31 | -9 | false |

```json
{
  "total": 353,
  "replacement_api": "scipy.stats.stats.ttest_ind",
  "threshold_10pct": 35.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 112,
      "score": 0.372665
    },
    "tokenBased": {
      "rank": 12,
      "score": 0.568548
    },
    "treeBased": {
      "rank": 22,
      "score": 0.463889
    }
  },
  "vi": {
    "mapBased": {
      "rank": 67,
      "score": 0.421394
    },
    "tokenBased": {
      "rank": 18,
      "score": 0.557692
    },
    "treeBased": {
      "rank": 31,
      "score": 0.453826
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 112,
      "vi_rank": 67,
      "delta": 45,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 12,
      "vi_rank": 18,
      "delta": -6,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 22,
      "vi_rank": 31,
      "delta": -9,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.13.3/scipy.stats.stats.ttest_ind.py`
- **new**: `R_candidates/Vi_v0.14.0/scipy.stats.stats.ttest_ind.py`
- **+3 / -0**

```diff
--- R_candidates/Vi-1_v0.13.3/scipy.stats.stats.ttest_ind.py
+++ R_candidates/Vi_v0.14.0/scipy.stats.stats.ttest_ind.py
@@ -1,6 +1,9 @@
 def ttest_ind(a, b, axis=0, equal_var=True):
     
     a, b, axis = _chk2_asarray(a, b, axis)
+    if a.size == 0 or b.size == 0:
+        return (np.nan, np.nan)
+
     v1 = np.var(a, axis, ddof=1)
     v2 = np.var(b, axis, ddof=1)
     n1 = a.shape[axis]
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.13.3/scipy.stats.stats.ttest_ind.py",
  "new_file": "R_candidates/Vi_v0.14.0/scipy.stats.stats.ttest_ind.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
