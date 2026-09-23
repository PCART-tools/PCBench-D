# 一、突变情况分析

- **Total**: 2392
- **替代API**: `matplotlib.cbook.normalize_kwargs`
- **10% 阈值**: 239.2

## Vi-1 (v3.2.2-v3.4.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 613 | 0.3261 |
| tokenBased | 1541 | 0.1865 |
| treeBased | 2191 | 0.2263 |

## Vi (v3.2.2-v3.5.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 176 | 0.4325 |
| tokenBased | 437 | 0.2778 |
| treeBased | 1599 | 0.3413 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 613 | 176 | +437 | true |
| tokenBased | 1541 | 437 | +1104 | true |
| treeBased | 2191 | 1599 | +592 | true |

```json
{
  "total": 2392,
  "replacement_api": "matplotlib.cbook.normalize_kwargs",
  "threshold_10pct": 239.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 613,
      "score": 0.326138
    },
    "tokenBased": {
      "rank": 1541,
      "score": 0.186528
    },
    "treeBased": {
      "rank": 2191,
      "score": 0.226277
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 613,
      "vi_rank": 176,
      "delta": 437,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1541,
      "vi_rank": 437,
      "delta": 1104,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2191,
      "vi_rank": 1599,
      "delta": 592,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v3.4.3/matplotlib.cbook.normalize_kwargs.py`
- **new**: `R_candidates/Vi_v3.5.0/matplotlib.cbook.normalize_kwargs.py`
- **+1 / -24**

```diff
--- R_candidates/Vi-1_v3.4.3/matplotlib.cbook.normalize_kwargs.py
+++ R_candidates/Vi_v3.5.0/matplotlib.cbook.normalize_kwargs.py
@@ -1,8 +1,4 @@
-@_api.delete_parameter("3.3", "required")
-@_api.delete_parameter("3.3", "forbidden")
-@_api.delete_parameter("3.3", "allowed")
-def normalize_kwargs(kw, alias_mapping=None, required=(), forbidden=(),
-                     allowed=None):
+def normalize_kwargs(kw, alias_mapping=None):
     
     from matplotlib.artist import Artist
 
@@ -30,23 +26,4 @@
         canonical_to_seen[canonical] = k
         ret[canonical] = v
 
-    fail_keys = [k for k in required if k not in ret]
-    if fail_keys:
-        raise TypeError("The required keys {keys!r} "
-                        "are not in kwargs".format(keys=fail_keys))
-
-    fail_keys = [k for k in forbidden if k in ret]
-    if fail_keys:
-        raise TypeError("The forbidden keys {keys!r} "
-                        "are in kwargs".format(keys=fail_keys))
-
-    if allowed is not None:
-        allowed_set = {*required, *allowed}
-        fail_keys = [k for k in ret if k not in allowed_set]
-        if fail_keys:
-            raise TypeError(
-                "kwargs contains {keys!r} which are not in the required "
-                "{req!r} or allowed {allow!r} keys".format(
-                    keys=fail_keys, req=required, allow=allowed))
-
     return ret
```

```json
{
  "old_file": "R_candidates/Vi-1_v3.4.3/matplotlib.cbook.normalize_kwargs.py",
  "new_file": "R_candidates/Vi_v3.5.0/matplotlib.cbook.normalize_kwargs.py",
  "lines_added": 1,
  "lines_removed": 24
}
```
