# 一、突变情况分析

- **Total**: 112
- **替代API**: `pandas.core.dtypes.common.is_datetime64tz_dtype`
- **10% 阈值**: 11.2

## Vi-1 (v0.23.4-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 38 | 0.5971 |
| tokenBased | 47 | 0.2955 |
| treeBased | 24 | 0.5227 |

## Vi (v0.24.0-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 32 | 0.7023 |
| tokenBased | 26 | 0.3611 |
| treeBased | 2 | 0.6053 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 38 | 32 | +6 | false |
| tokenBased | 47 | 26 | +21 | true |
| treeBased | 24 | 2 | +22 | true |

```json
{
  "total": 112,
  "replacement_api": "pandas.core.dtypes.common.is_datetime64tz_dtype",
  "threshold_10pct": 11.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 38,
      "score": 0.597107
    },
    "tokenBased": {
      "rank": 47,
      "score": 0.295455
    },
    "treeBased": {
      "rank": 24,
      "score": 0.522727
    }
  },
  "vi": {
    "mapBased": {
      "rank": 32,
      "score": 0.70229
    },
    "tokenBased": {
      "rank": 26,
      "score": 0.361111
    },
    "treeBased": {
      "rank": 2,
      "score": 0.605263
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 38,
      "vi_rank": 32,
      "delta": 6,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 47,
      "vi_rank": 26,
      "delta": 21,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 24,
      "vi_rank": 2,
      "delta": 22,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.dtypes.common.is_datetimetz/Vi-1_v0.23.4.py`
- **new**: `pandas.core.dtypes.common.is_datetimetz/Vi_v0.24.0.py`
- **+4 / -6**

```diff
--- pandas.core.dtypes.common.is_datetimetz/Vi-1_v0.23.4.py
+++ pandas.core.dtypes.common.is_datetimetz/Vi_v0.24.0.py
@@ -1,9 +1,7 @@
 def is_datetimetz(arr):
     
 
-
-
-
-    return ((isinstance(arr, ABCDatetimeIndex) and
-             getattr(arr, 'tz', None) is not None) or
-            is_datetime64tz_dtype(arr))
+    warnings.warn("'is_datetimetz' is deprecated and will be removed in a "
+                  "future version.  Use 'is_datetime64tz_dtype' instead.",
+                  FutureWarning, stacklevel=2)
+    return is_datetime64tz_dtype(arr)
```

```json
{
  "old_file": "pandas.core.dtypes.common.is_datetimetz/Vi-1_v0.23.4.py",
  "new_file": "pandas.core.dtypes.common.is_datetimetz/Vi_v0.24.0.py",
  "lines_added": 4,
  "lines_removed": 6
}
```
