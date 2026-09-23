# 一、突变情况分析

- **Total**: 430
- **替代API**: `polars.series.series.Series.map_elements`
- **10% 阈值**: 43.0

## Vi-1 (py-0.18.15-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9972 |
| tokenBased | 1 | 0.8395 |
| treeBased | 1 | 0.9516 |

## Vi (py-0.19.0-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 147 | 0.6557 |
| tokenBased | 1 | 0.5556 |
| treeBased | 3 | 0.6364 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 147 | -146 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 3 | -2 | false |

```json
{
  "total": 430,
  "replacement_api": "polars.series.series.Series.map_elements",
  "threshold_10pct": 43.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.997248
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.839506
    },
    "treeBased": {
      "rank": 1,
      "score": 0.951613
    }
  },
  "vi": {
    "mapBased": {
      "rank": 147,
      "score": 0.65567
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.555556
    },
    "treeBased": {
      "rank": 3,
      "score": 0.636364
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 147,
      "delta": -146,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 3,
      "delta": -2,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.series.series.Series.apply/Vi-1_py-0.18.15.py`
- **new**: `polars.series.series.Series.apply/Vi_py-0.19.0.py`
- **+2 / -11**

```diff
--- polars.series.series.Series.apply/Vi-1_py-0.18.15.py
+++ polars.series.series.Series.apply/Vi_py-0.19.0.py
@@ -1,3 +1,4 @@
+    @deprecate_renamed_function("map_elements", version="0.19.0")
     def apply(
         self,
         function: Callable[[Any], Any],
@@ -6,14 +7,4 @@
         skip_nulls: bool = True,
     ) -> Self:
         
-        from polars.utils.udfs import warn_on_inefficient_apply
-
-        if return_dtype is None:
-            pl_return_dtype = None
-        else:
-            pl_return_dtype = py_type_to_dtype(return_dtype)
-
-        warn_on_inefficient_apply(function, columns=[self.name], apply_target="series")
-        return self._from_pyseries(
-            self._s.apply_lambda(function, pl_return_dtype, skip_nulls)
-        )
+        return self.map_elements(function, return_dtype, skip_nulls=skip_nulls)
```

```json
{
  "old_file": "polars.series.series.Series.apply/Vi-1_py-0.18.15.py",
  "new_file": "polars.series.series.Series.apply/Vi_py-0.19.0.py",
  "lines_added": 2,
  "lines_removed": 11
}
```
