# 一、突变情况分析

- **Total**: 112
- **替代API**: `pandas.core.dtypes.common.is_datetime64tz_dtype`
- **10% 阈值**: 11.2

## Vi-1 (v0.23.4-v1.0.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 38 | 0.5971 |
| tokenBased | 47 | 0.2955 |
| treeBased | 24 | 0.5227 |

## Vi (v0.23.4-v1.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 46 | 0.5211 |
| tokenBased | 10 | 0.4167 |
| treeBased | 21 | 0.5357 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 38 | 46 | -8 | false |
| tokenBased | 47 | 10 | +37 | true |
| treeBased | 24 | 21 | +3 | false |

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
      "rank": 46,
      "score": 0.521104
    },
    "tokenBased": {
      "rank": 10,
      "score": 0.416667
    },
    "treeBased": {
      "rank": 21,
      "score": 0.535714
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 38,
      "vi_rank": 46,
      "delta": -8,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 47,
      "vi_rank": 10,
      "delta": 37,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 24,
      "vi_rank": 21,
      "delta": 3,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.0.5/pandas.core.dtypes.common.is_datetime64tz_dtype.py`
- **new**: `R_candidates/Vi_v1.1.0/pandas.core.dtypes.common.is_datetime64tz_dtype.py`
- **+3 / -0**

```diff
--- R_candidates/Vi-1_v1.0.5/pandas.core.dtypes.common.is_datetime64tz_dtype.py
+++ R_candidates/Vi_v1.1.0/pandas.core.dtypes.common.is_datetime64tz_dtype.py
@@ -1,5 +1,8 @@
 def is_datetime64tz_dtype(arr_or_dtype) -> bool:
     
+    if isinstance(arr_or_dtype, ExtensionDtype):
+
+        return arr_or_dtype.kind == "M"
 
     if arr_or_dtype is None:
         return False
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.0.5/pandas.core.dtypes.common.is_datetime64tz_dtype.py",
  "new_file": "R_candidates/Vi_v1.1.0/pandas.core.dtypes.common.is_datetime64tz_dtype.py",
  "lines_added": 3,
  "lines_removed": 0
}
```
