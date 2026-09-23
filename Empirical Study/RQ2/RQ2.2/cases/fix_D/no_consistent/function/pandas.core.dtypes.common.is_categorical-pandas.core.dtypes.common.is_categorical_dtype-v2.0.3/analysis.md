# 一、突变情况分析

- **Total**: 125
- **替代API**: `pandas.core.dtypes.common.is_categorical_dtype`
- **10% 阈值**: 12.5

## Vi-1 (v1.5.3-v2.0.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 57 | 0.4893 |
| tokenBased | 2 | 0.5556 |
| treeBased | 45 | 0.5088 |

## Vi (v1.5.3-v2.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 39 | 0.5761 |
| tokenBased | 2 | 0.6122 |
| treeBased | 4 | 0.6515 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 57 | 39 | +18 | true |
| tokenBased | 2 | 2 | +0 | false |
| treeBased | 45 | 4 | +41 | true |

```json
{
  "total": 125,
  "replacement_api": "pandas.core.dtypes.common.is_categorical_dtype",
  "threshold_10pct": 12.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 57,
      "score": 0.489329
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.555556
    },
    "treeBased": {
      "rank": 45,
      "score": 0.508772
    }
  },
  "vi": {
    "mapBased": {
      "rank": 39,
      "score": 0.576149
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.612245
    },
    "treeBased": {
      "rank": 4,
      "score": 0.651515
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 57,
      "vi_rank": 39,
      "delta": 18,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 2,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 45,
      "vi_rank": 4,
      "delta": 41,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v2.0.3/pandas.core.dtypes.common.is_categorical_dtype.py`
- **new**: `R_candidates/Vi_v2.1.0/pandas.core.dtypes.common.is_categorical_dtype.py`
- **+7 / -0**

```diff
--- R_candidates/Vi-1_v2.0.3/pandas.core.dtypes.common.is_categorical_dtype.py
+++ R_candidates/Vi_v2.1.0/pandas.core.dtypes.common.is_categorical_dtype.py
@@ -1,5 +1,12 @@
 def is_categorical_dtype(arr_or_dtype) -> bool:
     
+
+    warnings.warn(
+        "is_categorical_dtype is deprecated and will be removed in a future "
+        "version. Use isinstance(dtype, CategoricalDtype) instead",
+        FutureWarning,
+        stacklevel=find_stack_level(),
+    )
     if isinstance(arr_or_dtype, ExtensionDtype):
 
         return arr_or_dtype.name == "category"
```

```json
{
  "old_file": "R_candidates/Vi-1_v2.0.3/pandas.core.dtypes.common.is_categorical_dtype.py",
  "new_file": "R_candidates/Vi_v2.1.0/pandas.core.dtypes.common.is_categorical_dtype.py",
  "lines_added": 7,
  "lines_removed": 0
}
```
