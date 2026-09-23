# 一、突变情况分析

- **Total**: 2535
- **替代API**: `matplotlib.cbook.normalize_kwargs`
- **10% 阈值**: 253.5

## Vi-1 (v3.2.2-v3.5.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 176 | 0.4325 |
| tokenBased | 437 | 0.2778 |
| treeBased | 1599 | 0.3413 |

## Vi (v3.3.0-v3.5.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 833 | 0.2355 |
| tokenBased | 1671 | 0.0968 |
| treeBased | 1863 | 0.1986 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 176 | 833 | -657 | true |
| tokenBased | 437 | 1671 | -1234 | true |
| treeBased | 1599 | 1863 | -264 | true |

```json
{
  "total": 2535,
  "replacement_api": "matplotlib.cbook.normalize_kwargs",
  "threshold_10pct": 253.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 176,
      "score": 0.432513
    },
    "tokenBased": {
      "rank": 437,
      "score": 0.277778
    },
    "treeBased": {
      "rank": 1599,
      "score": 0.341317
    }
  },
  "vi": {
    "mapBased": {
      "rank": 833,
      "score": 0.235488
    },
    "tokenBased": {
      "rank": 1671,
      "score": 0.096774
    },
    "treeBased": {
      "rank": 1863,
      "score": 0.198582
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 176,
      "vi_rank": 833,
      "delta": -657,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 437,
      "vi_rank": 1671,
      "delta": -1234,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1599,
      "vi_rank": 1863,
      "delta": -264,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `matplotlib.cbook.local_over_kwdict/Vi-1_v3.2.2.py`
- **new**: `matplotlib.cbook.local_over_kwdict/Vi_v3.3.0.py`
- **+2 / -10**

```diff
--- matplotlib.cbook.local_over_kwdict/Vi-1_v3.2.2.py
+++ matplotlib.cbook.local_over_kwdict/Vi_v3.3.0.py
@@ -1,12 +1,4 @@
+@deprecated("3.3", alternative="normalize_kwargs")
 def local_over_kwdict(local_var, kwargs, *keys):
     
-    out = local_var
-    for key in keys:
-        kwarg_val = kwargs.pop(key, None)
-        if kwarg_val is not None:
-            if out is None:
-                out = kwarg_val
-            else:
-                _warn_external('"%s" keyword argument will be ignored' % key,
-                               IgnoredKeywordWarning)
-    return out
+    return _local_over_kwdict(local_var, kwargs, *keys, IgnoredKeywordWarning)
```

```json
{
  "old_file": "matplotlib.cbook.local_over_kwdict/Vi-1_v3.2.2.py",
  "new_file": "matplotlib.cbook.local_over_kwdict/Vi_v3.3.0.py",
  "lines_added": 2,
  "lines_removed": 10
}
```
