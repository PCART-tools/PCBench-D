# 一、突变情况分析

- **Total**: 300
- **替代API**: `scipy.linalg.matfuncs.expm`
- **10% 阈值**: 30.0

## Vi-1 (v0.12.1-v0.19.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 197 | 0.3006 |
| tokenBased | 206 | 0.2211 |
| treeBased | 184 | 0.3363 |

## Vi (v0.12.1-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 258 | 0.2334 |
| tokenBased | 285 | 0.1222 |
| treeBased | 277 | 0.2211 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 197 | 258 | -61 | true |
| tokenBased | 206 | 285 | -79 | true |
| treeBased | 184 | 277 | -93 | true |

```json
{
  "total": 300,
  "replacement_api": "scipy.linalg.matfuncs.expm",
  "threshold_10pct": 30.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 197,
      "score": 0.300587
    },
    "tokenBased": {
      "rank": 206,
      "score": 0.221053
    },
    "treeBased": {
      "rank": 184,
      "score": 0.336283
    }
  },
  "vi": {
    "mapBased": {
      "rank": 258,
      "score": 0.233438
    },
    "tokenBased": {
      "rank": 285,
      "score": 0.122222
    },
    "treeBased": {
      "rank": 277,
      "score": 0.221053
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 197,
      "vi_rank": 258,
      "delta": -61,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 206,
      "vi_rank": 285,
      "delta": -79,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 184,
      "vi_rank": 277,
      "delta": -93,
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
