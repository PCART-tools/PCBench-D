# 一、突变情况分析

- **Total**: 371
- **替代API**: `scipy.stats.stats.ttest_ind`
- **10% 阈值**: 37.1

## Vi-1 (v0.12.1-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 18 | 0.4931 |
| tokenBased | 68 | 0.4581 |
| treeBased | 79 | 0.4202 |

## Vi (v0.12.1-v0.16.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 57 | 0.4366 |
| tokenBased | 74 | 0.4375 |
| treeBased | 107 | 0.3946 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 18 | 57 | -39 | true |
| tokenBased | 68 | 74 | -6 | false |
| treeBased | 79 | 107 | -28 | false |

```json
{
  "total": 371,
  "replacement_api": "scipy.stats.stats.ttest_ind",
  "threshold_10pct": 37.1,
  "vi_minus_1": {
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
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 18,
      "vi_rank": 57,
      "delta": -39,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 68,
      "vi_rank": 74,
      "delta": -6,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 79,
      "vi_rank": 107,
      "delta": -28,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.16.0/scipy.stats.stats.ttest_ind.py`
- **new**: `R_candidates/Vi_v0.16.1/scipy.stats.stats.ttest_ind.py`
- **+0 / -2**

```diff
--- R_candidates/Vi-1_v0.16.0/scipy.stats.stats.ttest_ind.py
+++ R_candidates/Vi_v0.16.1/scipy.stats.stats.ttest_ind.py
@@ -1,8 +1,6 @@
 def ttest_ind(a, b, axis=0, equal_var=True):
     
     a, b, axis = _chk2_asarray(a, b, axis)
-
-    Ttest_indResult = namedtuple('Ttest_indResult', ('statistic', 'pvalue'))
 
     if a.size == 0 or b.size == 0:
         return Ttest_indResult(np.nan, np.nan)
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.16.0/scipy.stats.stats.ttest_ind.py",
  "new_file": "R_candidates/Vi_v0.16.1/scipy.stats.stats.ttest_ind.py",
  "lines_added": 0,
  "lines_removed": 2
}
```
