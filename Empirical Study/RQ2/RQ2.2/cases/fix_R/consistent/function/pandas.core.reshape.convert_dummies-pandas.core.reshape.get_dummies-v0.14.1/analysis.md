# 一、突变情况分析

- **Total**: 416
- **替代API**: `pandas.core.reshape.get_dummies`
- **10% 阈值**: 41.6

## Vi-1 (v0.14.1-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 344 | 0.2725 |
| tokenBased | 349 | 0.1801 |
| treeBased | 373 | 0.2500 |

## Vi (v0.15.0-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 238 | 0.3243 |
| tokenBased | 329 | 0.2085 |
| treeBased | 371 | 0.2831 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 344 | 238 | +106 | true |
| tokenBased | 349 | 329 | +20 | false |
| treeBased | 373 | 371 | +2 | false |

```json
{
  "total": 416,
  "replacement_api": "pandas.core.reshape.get_dummies",
  "threshold_10pct": 41.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 344,
      "score": 0.272545
    },
    "tokenBased": {
      "rank": 349,
      "score": 0.180095
    },
    "treeBased": {
      "rank": 373,
      "score": 0.25
    }
  },
  "vi": {
    "mapBased": {
      "rank": 238,
      "score": 0.324253
    },
    "tokenBased": {
      "rank": 329,
      "score": 0.208531
    },
    "treeBased": {
      "rank": 371,
      "score": 0.283088
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 344,
      "vi_rank": 238,
      "delta": 106,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 349,
      "vi_rank": 329,
      "delta": 20,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 373,
      "vi_rank": 371,
      "delta": 2,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.reshape.convert_dummies/Vi-1_v0.14.1.py`
- **new**: `pandas.core.reshape.convert_dummies/Vi_v0.15.0.py`
- **+8 / -2**

```diff
--- pandas.core.reshape.convert_dummies/Vi-1_v0.14.1.py
+++ pandas.core.reshape.convert_dummies/Vi_v0.15.0.py
@@ -1,8 +1,14 @@
 def convert_dummies(data, cat_variables, prefix_sep='_'):
     
+    import warnings
+
+    warnings.warn("'convert_dummies' is deprecated and will be removed "
+                  "in a future release. Use 'get_dummies' instead.",
+                  FutureWarning)
+
     result = data.drop(cat_variables, axis=1)
     for variable in cat_variables:
-        dummies = get_dummies(data[variable], prefix=variable,
-                              prefix_sep=prefix_sep)
+        dummies = _get_dummies_1d(data[variable], prefix=variable,
+                                  prefix_sep=prefix_sep)
         result = result.join(dummies)
     return result
```

```json
{
  "old_file": "pandas.core.reshape.convert_dummies/Vi-1_v0.14.1.py",
  "new_file": "pandas.core.reshape.convert_dummies/Vi_v0.15.0.py",
  "lines_added": 8,
  "lines_removed": 2
}
```
