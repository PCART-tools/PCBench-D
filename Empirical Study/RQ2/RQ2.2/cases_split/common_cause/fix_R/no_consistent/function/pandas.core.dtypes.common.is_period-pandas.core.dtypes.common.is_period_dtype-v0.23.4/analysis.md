# 一、突变情况分析

- **Total**: 112
- **替代API**: `pandas.core.dtypes.common.is_period_dtype`
- **10% 阈值**: 11.2

## Vi-1 (v0.23.4-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 38 | 0.5971 |
| tokenBased | 6 | 0.4545 |
| treeBased | 33 | 0.5429 |

## Vi (v0.24.0-v1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 41 | 0.5515 |
| tokenBased | 10 | 0.4103 |
| treeBased | 17 | 0.5349 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 38 | 41 | -3 | false |
| tokenBased | 6 | 10 | -4 | false |
| treeBased | 33 | 17 | +16 | true |

```json
{
  "total": 112,
  "replacement_api": "pandas.core.dtypes.common.is_period_dtype",
  "threshold_10pct": 11.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 38,
      "score": 0.597107
    },
    "tokenBased": {
      "rank": 6,
      "score": 0.454545
    },
    "treeBased": {
      "rank": 33,
      "score": 0.542857
    }
  },
  "vi": {
    "mapBased": {
      "rank": 41,
      "score": 0.551527
    },
    "tokenBased": {
      "rank": 10,
      "score": 0.410256
    },
    "treeBased": {
      "rank": 17,
      "score": 0.534884
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 38,
      "vi_rank": 41,
      "delta": -3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 6,
      "vi_rank": 10,
      "delta": -4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 33,
      "vi_rank": 17,
      "delta": 16,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.dtypes.common.is_period/Vi-1_v0.23.4.py`
- **new**: `pandas.core.dtypes.common.is_period/Vi_v0.24.0.py`
- **+3 / -1**

```diff
--- pandas.core.dtypes.common.is_period/Vi-1_v0.23.4.py
+++ pandas.core.dtypes.common.is_period/Vi_v0.24.0.py
@@ -1,6 +1,8 @@
 def is_period(arr):
     
 
-
+    warnings.warn("'is_period' is deprecated and will be removed in a future "
+                  "version.  Use 'is_period_dtype' or is_period_arraylike' "
+                  "instead.", FutureWarning, stacklevel=2)
 
     return isinstance(arr, ABCPeriodIndex) or is_period_arraylike(arr)
```

```json
{
  "old_file": "pandas.core.dtypes.common.is_period/Vi-1_v0.23.4.py",
  "new_file": "pandas.core.dtypes.common.is_period/Vi_v0.24.0.py",
  "lines_added": 3,
  "lines_removed": 1
}
```
