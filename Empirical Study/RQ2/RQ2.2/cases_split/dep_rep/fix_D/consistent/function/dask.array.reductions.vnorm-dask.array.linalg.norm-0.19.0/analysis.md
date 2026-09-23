# 一、突变情况分析

- **Total**: 1087
- **替代API**: `dask.array.linalg.norm`
- **10% 阈值**: 108.7

## Vi-1 (0.15.4-0.19.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 473 | 0.1261 |
| tokenBased | 631 | 0.2211 |
| treeBased | 526 | 0.3216 |

## Vi (0.15.4-0.19.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 516 | 0.1064 |
| tokenBased | 815 | 0.1818 |
| treeBased | 808 | 0.2787 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 473 | 516 | -43 | false |
| tokenBased | 631 | 815 | -184 | true |
| treeBased | 526 | 808 | -282 | true |

```json
{
  "total": 1087,
  "replacement_api": "dask.array.linalg.norm",
  "threshold_10pct": 108.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 473,
      "score": 0.126068
    },
    "tokenBased": {
      "rank": 631,
      "score": 0.22113
    },
    "treeBased": {
      "rank": 526,
      "score": 0.321617
    }
  },
  "vi": {
    "mapBased": {
      "rank": 516,
      "score": 0.106406
    },
    "tokenBased": {
      "rank": 815,
      "score": 0.181818
    },
    "treeBased": {
      "rank": 808,
      "score": 0.278689
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 473,
      "vi_rank": 516,
      "delta": -43,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 631,
      "vi_rank": 815,
      "delta": -184,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 526,
      "vi_rank": 808,
      "delta": -282,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.19.0/dask.array.linalg.norm.py`
- **new**: `R_candidates/Vi_0.19.1/dask.array.linalg.norm.py`
- **+22 / -8**

```diff
--- R_candidates/Vi-1_0.19.0/dask.array.linalg.norm.py
+++ R_candidates/Vi_0.19.1/dask.array.linalg.norm.py
@@ -1,14 +1,14 @@
 @wraps(np.linalg.norm)
 def norm(x, ord=None, axis=None, keepdims=False):
-    if x.ndim > 2:
-        raise ValueError("Improper number of dimensions to norm.")
-
     if axis is None:
         axis = tuple(range(x.ndim))
     elif isinstance(axis, Number):
         axis = (int(axis),)
     else:
         axis = tuple(axis)
+
+    if len(axis) > 2:
+        raise ValueError("Improper number of dimensions to norm.")
 
     if ord == "fro":
         ord = None
@@ -23,6 +23,8 @@
     elif ord == "nuc":
         if len(axis) == 1:
             raise ValueError("Invalid norm order for vectors.")
+        if x.ndim > 2:
+            raise NotImplementedError("SVD based norm not implemented for ndim > 2")
 
         r = svd(x)[1][None].sum(keepdims=keepdims)
     elif ord == np.inf:
@@ -30,29 +32,41 @@
         if len(axis) == 1:
             r = r.max(axis=axis, keepdims=keepdims)
         else:
-            r = r.sum(axis=axis[1], keepdims=keepdims).max(keepdims=keepdims)
+            r = r.sum(axis=axis[1], keepdims=True).max(axis=axis[0], keepdims=True)
+            if keepdims is False:
+                r = r.squeeze(axis=axis)
     elif ord == -np.inf:
         r = abs(r)
         if len(axis) == 1:
             r = r.min(axis=axis, keepdims=keepdims)
         else:
-            r = r.sum(axis=axis[1], keepdims=keepdims).min(keepdims=keepdims)
+            r = r.sum(axis=axis[1], keepdims=True).min(axis=axis[0], keepdims=True)
+            if keepdims is False:
+                r = r.squeeze(axis=axis)
     elif ord == 0:
         if len(axis) == 2:
             raise ValueError("Invalid norm order for matrices.")
 
-        r = (r != 0).astype(r.dtype).sum(axis=0, keepdims=keepdims)
+        r = (r != 0).astype(r.dtype).sum(axis=axis, keepdims=keepdims)
     elif ord == 1:
         r = abs(r)
         if len(axis) == 1:
             r = r.sum(axis=axis, keepdims=keepdims)
         else:
-            r = r.sum(axis=axis[0], keepdims=keepdims).max(keepdims=keepdims)
+            r = r.sum(axis=axis[0], keepdims=True).max(axis=axis[1], keepdims=True)
+            if keepdims is False:
+                r = r.squeeze(axis=axis)
     elif len(axis) == 2 and ord == -1:
-        r = abs(r).sum(axis=axis[0], keepdims=keepdims).min(keepdims=keepdims)
+        r = abs(r).sum(axis=axis[0], keepdims=True).min(axis=axis[1], keepdims=True)
+        if keepdims is False:
+            r = r.squeeze(axis=axis)
     elif len(axis) == 2 and ord == 2:
+        if x.ndim > 2:
+            raise NotImplementedError("SVD based norm not implemented for ndim > 2")
         r = svd(x)[1][None].max(keepdims=keepdims)
     elif len(axis) == 2 and ord == -2:
+        if x.ndim > 2:
+            raise NotImplementedError("SVD based norm not implemented for ndim > 2")
         r = svd(x)[1][None].min(keepdims=keepdims)
     else:
         if len(axis) == 2:
```

```json
{
  "old_file": "R_candidates/Vi-1_0.19.0/dask.array.linalg.norm.py",
  "new_file": "R_candidates/Vi_0.19.1/dask.array.linalg.norm.py",
  "lines_added": 22,
  "lines_removed": 8
}
```
