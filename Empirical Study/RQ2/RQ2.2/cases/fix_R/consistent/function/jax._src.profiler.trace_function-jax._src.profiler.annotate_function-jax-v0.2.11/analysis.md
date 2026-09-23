# 一、突变情况分析

- **Total**: 2276
- **替代API**: `jax._src.profiler.annotate_function`
- **10% 阈值**: 227.6

## Vi-1 (jax-v0.2.11-jax-v0.3.15)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8154 |
| treeBased | 1 | 0.9561 |

## Vi (jax-v0.2.12-jax-v0.3.15)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1029 | 0.5125 |
| tokenBased | 529 | 0.2388 |
| treeBased | 925 | 0.4026 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 1029 | -1028 | true |
| tokenBased | 1 | 529 | -528 | true |
| treeBased | 1 | 925 | -924 | true |

```json
{
  "total": 2276,
  "replacement_api": "jax._src.profiler.annotate_function",
  "threshold_10pct": 227.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.815385
    },
    "treeBased": {
      "rank": 1,
      "score": 0.95614
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1029,
      "score": 0.512461
    },
    "tokenBased": {
      "rank": 529,
      "score": 0.238806
    },
    "treeBased": {
      "rank": 925,
      "score": 0.402597
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 1029,
      "delta": -1028,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 529,
      "delta": -528,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 925,
      "delta": -924,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.profiler.trace_function/Vi-1_jax-v0.2.11.py`
- **new**: `jax._src.profiler.trace_function/Vi_jax-v0.2.12.py`
- **+5 / -11**

```diff
--- jax._src.profiler.trace_function/Vi-1_jax-v0.2.11.py
+++ jax._src.profiler.trace_function/Vi_jax-v0.2.12.py
@@ -1,11 +1,5 @@
-def trace_function(func: Callable, name: str = None, **kwargs):
-  
-
-  name = name or getattr(func, '__qualname__', None)
-  name = name or func.__name__
-  @wraps(func)
-  def wrapper(*args, **kwargs):
-    with TraceContext(name, **kwargs):
-      return func(*args, **kwargs)
-    return wrapper
-  return wrapper
+def trace_function(*args, **kwargs):
+  warnings.warn(
+      "trace_function has been renamed to annotate_function. This alias "
+      "will eventually be removed; please update your code.")
+  return annotate_function(*args, **kwargs)
```

```json
{
  "old_file": "jax._src.profiler.trace_function/Vi-1_jax-v0.2.11.py",
  "new_file": "jax._src.profiler.trace_function/Vi_jax-v0.2.12.py",
  "lines_added": 5,
  "lines_removed": 11
}
```
