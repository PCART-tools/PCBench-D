# 一、突变情况分析

- **Total**: 66
- **替代API**: `networkx.utils.misc.dict_to_numpy_array`
- **10% 阈值**: 6.6

## Vi-1 (networkx-2.7.1-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 17 | 0.3052 |
| tokenBased | 23 | 0.2636 |
| treeBased | 39 | 0.3089 |

## Vi (networkx-2.8-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 10 | 0.5863 |
| tokenBased | 1 | 0.7027 |
| treeBased | 2 | 0.6275 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 17 | 10 | +7 | true |
| tokenBased | 23 | 1 | +22 | true |
| treeBased | 39 | 2 | +37 | true |

```json
{
  "total": 66,
  "replacement_api": "networkx.utils.misc.dict_to_numpy_array",
  "threshold_10pct": 6.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 17,
      "score": 0.305195
    },
    "tokenBased": {
      "rank": 23,
      "score": 0.263636
    },
    "treeBased": {
      "rank": 39,
      "score": 0.308943
    }
  },
  "vi": {
    "mapBased": {
      "rank": 10,
      "score": 0.586301
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.702703
    },
    "treeBased": {
      "rank": 2,
      "score": 0.627451
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 17,
      "vi_rank": 10,
      "delta": 7,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 23,
      "vi_rank": 1,
      "delta": 22,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 39,
      "vi_rank": 2,
      "delta": 37,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.utils.misc.dict_to_numpy_array2/Vi-1_networkx-2.7.1.py`
- **new**: `networkx.utils.misc.dict_to_numpy_array2/Vi_networkx-2.8.py`
- **+7 / -14**

```diff
--- networkx.utils.misc.dict_to_numpy_array2/Vi-1_networkx-2.7.1.py
+++ networkx.utils.misc.dict_to_numpy_array2/Vi_networkx-2.8.py
@@ -1,16 +1,9 @@
 def dict_to_numpy_array2(d, mapping=None):
     
-    if mapping is None:
-        s = set(d.keys())
-        for k, v in d.items():
-            s.update(v.keys())
-        mapping = dict(zip(s, range(len(s))))
-    n = len(mapping)
-    a = np.zeros((n, n))
-    for k1, i in mapping.items():
-        for k2, j in mapping.items():
-            try:
-                a[i, j] = d[k1][k2]
-            except KeyError:
-                pass
-    return a
+    msg = (
+        "dict_to_numpy_array2 is deprecated and will be removed in networkx 3.0.\n"
+        "Use dict_to_numpy_array instead."
+    )
+    warnings.warn(msg, DeprecationWarning, stacklevel=2)
+
+    return _dict_to_numpy_array2(d, mapping)
```

```json
{
  "old_file": "networkx.utils.misc.dict_to_numpy_array2/Vi-1_networkx-2.7.1.py",
  "new_file": "networkx.utils.misc.dict_to_numpy_array2/Vi_networkx-2.8.py",
  "lines_added": 7,
  "lines_removed": 14
}
```
