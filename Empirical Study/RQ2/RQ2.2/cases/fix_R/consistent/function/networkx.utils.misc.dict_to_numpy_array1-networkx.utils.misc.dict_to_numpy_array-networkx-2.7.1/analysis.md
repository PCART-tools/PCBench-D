# 一、突变情况分析

- **Total**: 66
- **替代API**: `networkx.utils.misc.dict_to_numpy_array`
- **10% 阈值**: 6.6

## Vi-1 (networkx-2.7.1-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 38 | 0.2763 |
| tokenBased | 23 | 0.3214 |
| treeBased | 28 | 0.3978 |

## Vi (networkx-2.8-networkx-3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 10 | 0.5863 |
| tokenBased | 1 | 0.7027 |
| treeBased | 1 | 0.6471 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 38 | 10 | +28 | true |
| tokenBased | 23 | 1 | +22 | true |
| treeBased | 28 | 1 | +27 | true |

```json
{
  "total": 66,
  "replacement_api": "networkx.utils.misc.dict_to_numpy_array",
  "threshold_10pct": 6.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 38,
      "score": 0.276316
    },
    "tokenBased": {
      "rank": 23,
      "score": 0.321429
    },
    "treeBased": {
      "rank": 28,
      "score": 0.397849
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
      "rank": 1,
      "score": 0.647059
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 38,
      "vi_rank": 10,
      "delta": 28,
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
      "vi1_rank": 28,
      "vi_rank": 1,
      "delta": 27,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.utils.misc.dict_to_numpy_array1/Vi-1_networkx-2.7.1.py`
- **new**: `networkx.utils.misc.dict_to_numpy_array1/Vi_networkx-2.8.py`
- **+7 / -9**

```diff
--- networkx.utils.misc.dict_to_numpy_array1/Vi-1_networkx-2.7.1.py
+++ networkx.utils.misc.dict_to_numpy_array1/Vi_networkx-2.8.py
@@ -1,11 +1,9 @@
 def dict_to_numpy_array1(d, mapping=None):
     
-    if mapping is None:
-        s = set(d.keys())
-        mapping = dict(zip(s, range(len(s))))
-    n = len(mapping)
-    a = np.zeros(n)
-    for k1, i in mapping.items():
-        i = mapping[k1]
-        a[i] = d[k1]
-    return a
+    msg = (
+        "dict_to_numpy_array1 is deprecated and will be removed in networkx 3.0.\n"
+        "Use dict_to_numpy_array instead."
+    )
+    warnings.warn(msg, DeprecationWarning, stacklevel=2)
+
+    return _dict_to_numpy_array1(d, mapping)
```

```json
{
  "old_file": "networkx.utils.misc.dict_to_numpy_array1/Vi-1_networkx-2.7.1.py",
  "new_file": "networkx.utils.misc.dict_to_numpy_array1/Vi_networkx-2.8.py",
  "lines_added": 7,
  "lines_removed": 9
}
```
