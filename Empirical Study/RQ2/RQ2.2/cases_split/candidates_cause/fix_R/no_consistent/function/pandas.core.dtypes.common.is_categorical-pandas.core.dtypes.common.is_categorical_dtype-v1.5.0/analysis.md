# 一、突变情况分析

- **Total**: 124
- **替代API**: `pandas.core.dtypes.common.is_categorical_dtype`
- **10% 阈值**: 12.4

## Vi-1 (v1.5.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 57 | 0.4893 |
| tokenBased | 6 | 0.5417 |
| treeBased | 30 | 0.5167 |

## Vi (v1.5.1-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 57 | 0.4893 |
| tokenBased | 2 | 0.5556 |
| treeBased | 45 | 0.5088 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 57 | 57 | +0 | false |
| tokenBased | 6 | 2 | +4 | false |
| treeBased | 30 | 45 | -15 | true |

```json
{
  "total": 124,
  "replacement_api": "pandas.core.dtypes.common.is_categorical_dtype",
  "threshold_10pct": 12.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 57,
      "score": 0.489329
    },
    "tokenBased": {
      "rank": 6,
      "score": 0.541667
    },
    "treeBased": {
      "rank": 30,
      "score": 0.516667
    }
  },
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 57,
      "vi_rank": 57,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 6,
      "vi_rank": 2,
      "delta": 4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 30,
      "vi_rank": 45,
      "delta": -15,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.dtypes.common.is_categorical/Vi-1_v1.5.0.py`
- **new**: `pandas.core.dtypes.common.is_categorical/Vi_v1.5.1.py`
- **+1 / -1**

```diff
--- pandas.core.dtypes.common.is_categorical/Vi-1_v1.5.0.py
+++ pandas.core.dtypes.common.is_categorical/Vi_v1.5.1.py
@@ -4,6 +4,6 @@
         "is_categorical is deprecated and will be removed in a future version. "
         "Use is_categorical_dtype instead.",
         FutureWarning,
-        stacklevel=find_stack_level(inspect.currentframe()),
+        stacklevel=find_stack_level(),
     )
     return isinstance(arr, ABCCategorical) or is_categorical_dtype(arr)
```

```json
{
  "old_file": "pandas.core.dtypes.common.is_categorical/Vi-1_v1.5.0.py",
  "new_file": "pandas.core.dtypes.common.is_categorical/Vi_v1.5.1.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
