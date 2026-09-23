# 一、突变情况分析

- **Total**: 312
- **替代API**: `scipy.linalg.matfuncs.expm`
- **10% 阈值**: 31.2

## Vi-1 (v0.8.0-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 198 | 0.3314 |
| tokenBased | 276 | 0.1486 |
| treeBased | 245 | 0.2857 |

## Vi (v0.9.0-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 258 | 0.2334 |
| tokenBased | 285 | 0.1222 |
| treeBased | 277 | 0.2211 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 198 | 258 | -60 | true |
| tokenBased | 276 | 285 | -9 | false |
| treeBased | 245 | 277 | -32 | true |

```json
{
  "total": 312,
  "replacement_api": "scipy.linalg.matfuncs.expm",
  "threshold_10pct": 31.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 198,
      "score": 0.331361
    },
    "tokenBased": {
      "rank": 276,
      "score": 0.148649
    },
    "treeBased": {
      "rank": 245,
      "score": 0.285714
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
      "vi1_rank": 198,
      "vi_rank": 258,
      "delta": -60,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 276,
      "vi_rank": 285,
      "delta": -9,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 245,
      "vi_rank": 277,
      "delta": -32,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `scipy.linalg.matfuncs.expm2/Vi-1_v0.8.0.py`
- **new**: `scipy.linalg.matfuncs.expm2/Vi_v0.9.0.py`
- **+5 / -1**

```diff
--- scipy.linalg.matfuncs.expm2/Vi-1_v0.8.0.py
+++ scipy.linalg.matfuncs.expm2/Vi_v0.9.0.py
@@ -8,4 +8,8 @@
         t = 'd'
     s,vr = eig(A)
     vri = inv(vr)
-    return dot(dot(vr,diag(exp(s))),vri).astype(t)
+    r = dot(dot(vr,diag(exp(s))),vri)
+    if t in ['f', 'd']:
+        return r.real.astype(t)
+    else:
+        return r.astype(t)
```

```json
{
  "old_file": "scipy.linalg.matfuncs.expm2/Vi-1_v0.8.0.py",
  "new_file": "scipy.linalg.matfuncs.expm2/Vi_v0.9.0.py",
  "lines_added": 5,
  "lines_removed": 1
}
```
