# 一、突变情况分析

- **Total**: 151
- **替代API**: `jax._src.profiler.TraceAnnotation`
- **10% 阈值**: 15.1

## Vi-1 (jax-v0.2.11-jax-v0.3.15)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.8500 |
| tokenBased | 1 | 0.6250 |

## Vi (jax-v0.2.12-jax-v0.3.15)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 39 | 0.2500 |
| tokenBased | 28 | 0.2368 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 39 | -38 | true |
| tokenBased | 1 | 28 | -27 | true |

```json
{
  "total": 151,
  "replacement_api": "jax._src.profiler.TraceAnnotation",
  "threshold_10pct": 15.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.85
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.625
    }
  },
  "vi": {
    "mapBased": {
      "rank": 39,
      "score": 0.25
    },
    "tokenBased": {
      "rank": 28,
      "score": 0.236842
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 39,
      "delta": -38,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 28,
      "delta": -27,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `jax._src.profiler.TraceContext/Vi-1_jax-v0.2.11.py`
- **new**: `jax._src.profiler.TraceContext/Vi_jax-v0.2.12.py`
- **+6 / -3**

```diff
--- jax._src.profiler.TraceContext/Vi-1_jax-v0.2.11.py
+++ jax._src.profiler.TraceContext/Vi_jax-v0.2.12.py
@@ -1,3 +1,6 @@
-class TraceContext(xla_client.profiler.TraceMe):
-  
-  pass
+class TraceContext(TraceAnnotation):
+  def __init__(self, *args, **kwargs):
+    warnings.warn(
+        "TraceContext has been renamed to TraceAnnotation. This alias "
+        "will eventually be removed; please update your code.")
+    super().__init__(*args, **kwargs)
```

```json
{
  "old_file": "jax._src.profiler.TraceContext/Vi-1_jax-v0.2.11.py",
  "new_file": "jax._src.profiler.TraceContext/Vi_jax-v0.2.12.py",
  "lines_added": 6,
  "lines_removed": 3
}
```
