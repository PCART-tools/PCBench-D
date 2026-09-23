# 一、突变情况分析

- **Total**: 248
- **替代API**: `scipy.integrate._quadrature.simpson`
- **10% 阈值**: 24.8

## Vi-1 (v1.11.4-v1.14.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 193 | 0.1093 |
| tokenBased | 233 | 0.0403 |
| treeBased | 238 | 0.0828 |

## Vi (v1.11.4-v1.15.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 220 | 0.1093 |
| tokenBased | 259 | 0.0403 |
| treeBased | 261 | 0.0868 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 193 | 220 | -27 | true |
| tokenBased | 233 | 259 | -26 | true |
| treeBased | 238 | 261 | -23 | false |

```json
{
  "total": 248,
  "replacement_api": "scipy.integrate._quadrature.simpson",
  "threshold_10pct": 24.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 193,
      "score": 0.109266
    },
    "tokenBased": {
      "rank": 233,
      "score": 0.04034
    },
    "treeBased": {
      "rank": 238,
      "score": 0.08284
    }
  },
  "vi": {
    "mapBased": {
      "rank": 220,
      "score": 0.109266
    },
    "tokenBased": {
      "rank": 259,
      "score": 0.04034
    },
    "treeBased": {
      "rank": 261,
      "score": 0.086785
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 193,
      "vi_rank": 220,
      "delta": -27,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 233,
      "vi_rank": 259,
      "delta": -26,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 238,
      "vi_rank": 261,
      "delta": -23,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.14.1/scipy.integrate._quadrature.simpson.py`
- **new**: `R_candidates/Vi_v1.15.0/scipy.integrate._quadrature.simpson.py`
- **+1 / -1**

```diff
--- R_candidates/Vi-1_v1.14.1/scipy.integrate._quadrature.simpson.py
+++ R_candidates/Vi_v1.15.0/scipy.integrate._quadrature.simpson.py
@@ -1,4 +1,4 @@
-def simpson(y, *, x=None, dx=1.0, axis=-1):
+def simpson(y, x=None, *, dx=1.0, axis=-1):
     
     y = np.asarray(y)
     nd = len(y.shape)
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.14.1/scipy.integrate._quadrature.simpson.py",
  "new_file": "R_candidates/Vi_v1.15.0/scipy.integrate._quadrature.simpson.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
