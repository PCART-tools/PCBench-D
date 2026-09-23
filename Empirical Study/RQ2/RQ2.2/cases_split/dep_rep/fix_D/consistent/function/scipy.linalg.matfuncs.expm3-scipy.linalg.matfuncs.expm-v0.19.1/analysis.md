# 一、突变情况分析

- **Total**: 300
- **替代API**: `scipy.linalg.matfuncs.expm`
- **10% 阈值**: 30.0

## Vi-1 (v0.12.1-v0.19.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 170 | 0.3482 |
| tokenBased | 200 | 0.2340 |
| treeBased | 172 | 0.3613 |

## Vi (v0.12.1-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 272 | 0.2419 |
| tokenBased | 292 | 0.1222 |
| treeBased | 296 | 0.1980 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 170 | 272 | -102 | true |
| tokenBased | 200 | 292 | -92 | true |
| treeBased | 172 | 296 | -124 | true |

```json
{
  "total": 300,
  "replacement_api": "scipy.linalg.matfuncs.expm",
  "threshold_10pct": 30.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 170,
      "score": 0.348214
    },
    "tokenBased": {
      "rank": 200,
      "score": 0.234043
    },
    "treeBased": {
      "rank": 172,
      "score": 0.361345
    }
  },
  "vi": {
    "mapBased": {
      "rank": 272,
      "score": 0.241912
    },
    "tokenBased": {
      "rank": 292,
      "score": 0.122222
    },
    "treeBased": {
      "rank": 296,
      "score": 0.19802
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 170,
      "vi_rank": 272,
      "delta": -102,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 200,
      "vi_rank": 292,
      "delta": -92,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 172,
      "vi_rank": 296,
      "delta": -124,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.19.1/scipy.linalg.matfuncs.expm.py`
- **new**: `R_candidates/Vi_v1.0.0/scipy.linalg.matfuncs.expm.py`
- **+1 / -4**

```diff
--- R_candidates/Vi-1_v0.19.1/scipy.linalg.matfuncs.expm.py
+++ R_candidates/Vi_v1.0.0/scipy.linalg.matfuncs.expm.py
@@ -1,8 +1,5 @@
-def expm(A, q=None):
+def expm(A):
     
-    if q is not None:
-        msg = "argument q=... in scipy.linalg.expm is deprecated." 
-        warnings.warn(msg, DeprecationWarning)
 
     import scipy.sparse.linalg
     return scipy.sparse.linalg.expm(A)
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.19.1/scipy.linalg.matfuncs.expm.py",
  "new_file": "R_candidates/Vi_v1.0.0/scipy.linalg.matfuncs.expm.py",
  "lines_added": 1,
  "lines_removed": 4
}
```
