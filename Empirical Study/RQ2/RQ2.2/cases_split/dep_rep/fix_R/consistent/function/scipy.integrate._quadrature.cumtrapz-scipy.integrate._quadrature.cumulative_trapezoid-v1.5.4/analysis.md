# 一、突变情况分析

- **Total**: 248
- **替代API**: `scipy.integrate._quadrature.cumulative_trapezoid`
- **10% 阈值**: 24.8

## Vi-1 (v1.5.4-v1.14.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.7375 |
| tokenBased | 1 | 0.8699 |
| treeBased | 1 | 0.9398 |

## Vi (v1.6.0-v1.14.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 154 | 0.2054 |
| tokenBased | 189 | 0.0810 |
| treeBased | 176 | 0.1913 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 154 | -153 | true |
| tokenBased | 1 | 189 | -188 | true |
| treeBased | 1 | 176 | -175 | true |

```json
{
  "total": 248,
  "replacement_api": "scipy.integrate._quadrature.cumulative_trapezoid",
  "threshold_10pct": 24.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.73749
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.869919
    },
    "treeBased": {
      "rank": 1,
      "score": 0.939785
    }
  },
  "vi": {
    "mapBased": {
      "rank": 154,
      "score": 0.2054
    },
    "tokenBased": {
      "rank": 189,
      "score": 0.080972
    },
    "treeBased": {
      "rank": 176,
      "score": 0.191336
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 154,
      "delta": -153,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 189,
      "delta": -188,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 176,
      "delta": -175,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `scipy.integrate._quadrature.cumtrapz/Vi-1_v1.5.4.py`
- **new**: `scipy.integrate._quadrature.cumtrapz/Vi_v1.6.0.py`
- **+1 / -36**

```diff
--- scipy.integrate._quadrature.cumtrapz/Vi-1_v1.5.4.py
+++ scipy.integrate._quadrature.cumtrapz/Vi_v1.6.0.py
@@ -1,38 +1,3 @@
 def cumtrapz(y, x=None, dx=1.0, axis=-1, initial=None):
     
-    y = np.asarray(y)
-    if x is None:
-        d = dx
-    else:
-        x = np.asarray(x)
-        if x.ndim == 1:
-            d = np.diff(x)
-
-            shape = [1] * y.ndim
-            shape[axis] = -1
-            d = d.reshape(shape)
-        elif len(x.shape) != len(y.shape):
-            raise ValueError("If given, shape of x must be 1-D or the "
-                             "same as y.")
-        else:
-            d = np.diff(x, axis=axis)
-
-        if d.shape[axis] != y.shape[axis] - 1:
-            raise ValueError("If given, length of x along axis must be the "
-                             "same as y.")
-
-    nd = len(y.shape)
-    slice1 = tupleset((slice(None),)*nd, axis, slice(1, None))
-    slice2 = tupleset((slice(None),)*nd, axis, slice(None, -1))
-    res = np.cumsum(d * (y[slice1] + y[slice2]) / 2.0, axis=axis)
-
-    if initial is not None:
-        if not np.isscalar(initial):
-            raise ValueError("`initial` parameter should be a scalar.")
-
-        shape = list(res.shape)
-        shape[axis] = 1
-        res = np.concatenate([np.full(shape, initial, dtype=res.dtype), res],
-                             axis=axis)
-
-    return res
+    return cumulative_trapezoid(y, x=x, dx=dx, axis=axis, initial=initial)
```

```json
{
  "old_file": "scipy.integrate._quadrature.cumtrapz/Vi-1_v1.5.4.py",
  "new_file": "scipy.integrate._quadrature.cumtrapz/Vi_v1.6.0.py",
  "lines_added": 1,
  "lines_removed": 36
}
```
