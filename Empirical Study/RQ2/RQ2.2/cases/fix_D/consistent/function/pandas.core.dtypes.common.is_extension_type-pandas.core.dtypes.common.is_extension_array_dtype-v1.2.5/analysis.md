# 一、突变情况分析

- **Total**: 115
- **替代API**: `pandas.core.dtypes.common.is_extension_array_dtype`
- **10% 阈值**: 11.5

## Vi-1 (v0.25.3-v1.2.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 78 | 0.3586 |
| tokenBased | 11 | 0.3774 |
| treeBased | 43 | 0.4655 |

## Vi (v0.25.3-v1.3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 6 | 0.6638 |
| tokenBased | 2 | 0.4483 |
| treeBased | 6 | 0.6111 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 78 | 6 | +72 | true |
| tokenBased | 11 | 2 | +9 | false |
| treeBased | 43 | 6 | +37 | true |

```json
{
  "total": 115,
  "replacement_api": "pandas.core.dtypes.common.is_extension_array_dtype",
  "threshold_10pct": 11.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 78,
      "score": 0.358561
    },
    "tokenBased": {
      "rank": 11,
      "score": 0.377358
    },
    "treeBased": {
      "rank": 43,
      "score": 0.465517
    }
  },
  "vi": {
    "mapBased": {
      "rank": 6,
      "score": 0.663776
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.448276
    },
    "treeBased": {
      "rank": 6,
      "score": 0.611111
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 78,
      "vi_rank": 6,
      "delta": 72,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 11,
      "vi_rank": 2,
      "delta": 9,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 43,
      "vi_rank": 6,
      "delta": 37,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.2.5/pandas.core.dtypes.common.is_extension_array_dtype.py`
- **new**: `R_candidates/Vi_v1.3.0/pandas.core.dtypes.common.is_extension_array_dtype.py`
- **+6 / -1**

```diff
--- R_candidates/Vi-1_v1.2.5/pandas.core.dtypes.common.is_extension_array_dtype.py
+++ R_candidates/Vi_v1.3.0/pandas.core.dtypes.common.is_extension_array_dtype.py
@@ -1,4 +1,9 @@
 def is_extension_array_dtype(arr_or_dtype) -> bool:
     
     dtype = getattr(arr_or_dtype, "dtype", arr_or_dtype)
-    return isinstance(dtype, ExtensionDtype) or registry.find(dtype) is not None
+    if isinstance(dtype, ExtensionDtype):
+        return True
+    elif isinstance(dtype, np.dtype):
+        return False
+    else:
+        return registry.find(dtype) is not None
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.2.5/pandas.core.dtypes.common.is_extension_array_dtype.py",
  "new_file": "R_candidates/Vi_v1.3.0/pandas.core.dtypes.common.is_extension_array_dtype.py",
  "lines_added": 6,
  "lines_removed": 1
}
```
