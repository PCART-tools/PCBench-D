# 一、突变情况分析

- **Total**: 403
- **替代API**: `dask.array.core.from_delayed`
- **10% 阈值**: 40.3

## Vi-1 (0.8.2-0.11.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.9118 |
| treeBased | 1 | 0.9919 |

## Vi (0.9.0-0.11.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 114 | 0.4445 |
| tokenBased | 82 | 0.1944 |
| treeBased | 158 | 0.3250 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 114 | -113 | true |
| tokenBased | 1 | 82 | -81 | true |
| treeBased | 1 | 158 | -157 | true |

```json
{
  "total": 403,
  "replacement_api": "dask.array.core.from_delayed",
  "threshold_10pct": 40.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.911765
    },
    "treeBased": {
      "rank": 1,
      "score": 0.991935
    }
  },
  "vi": {
    "mapBased": {
      "rank": 114,
      "score": 0.444474
    },
    "tokenBased": {
      "rank": 82,
      "score": 0.194444
    },
    "treeBased": {
      "rank": 158,
      "score": 0.325
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 114,
      "delta": -113,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 82,
      "delta": -81,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 158,
      "delta": -157,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `dask.array.core.from_imperative/Vi-1_0.8.2.py`
- **new**: `dask.array.core.from_imperative/Vi_0.9.0.py`
- **+3 / -7**

```diff
--- dask.array.core.from_imperative/Vi-1_0.8.2.py
+++ dask.array.core.from_imperative/Vi_0.9.0.py
@@ -1,7 +1,3 @@
-def from_imperative(value, shape, dtype=None, name=None):
-    
-    name = name or 'from-value-' + tokenize(value, shape, dtype)
-    dsk = {(name,) + (0,) * len(shape): value.key}
-    dsk.update(value.dask)
-    chunks = tuple((d,) for d in shape)
-    return Array(dsk, name, chunks, dtype)
+def from_imperative(*args, **kwargs):
+    warn("Deprecation warning: moved to from_delayed")
+    return from_delayed(*args, **kwargs)
```

```json
{
  "old_file": "dask.array.core.from_imperative/Vi-1_0.8.2.py",
  "new_file": "dask.array.core.from_imperative/Vi_0.9.0.py",
  "lines_added": 3,
  "lines_removed": 7
}
```
