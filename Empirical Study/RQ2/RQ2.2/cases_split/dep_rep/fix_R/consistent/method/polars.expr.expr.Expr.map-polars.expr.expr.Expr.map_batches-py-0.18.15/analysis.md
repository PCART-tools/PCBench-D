# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.expr.Expr.map_batches`
- **10% 阈值**: 45.7

## Vi-1 (py-0.18.15-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.9068 |
| tokenBased | 1 | 0.6979 |
| treeBased | 1 | 0.8364 |

## Vi (py-0.19.0-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 296 | 0.6839 |
| tokenBased | 2 | 0.5789 |
| treeBased | 2 | 0.6436 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2 | 296 | -294 | true |
| tokenBased | 1 | 2 | -1 | false |
| treeBased | 1 | 2 | -1 | false |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.expr.Expr.map_batches",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2,
      "score": 0.906822
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.697917
    },
    "treeBased": {
      "rank": 1,
      "score": 0.836364
    }
  },
  "vi": {
    "mapBased": {
      "rank": 296,
      "score": 0.683871
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.578947
    },
    "treeBased": {
      "rank": 2,
      "score": 0.643564
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2,
      "vi_rank": 296,
      "delta": -294,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.expr.Expr.map/Vi-1_py-0.18.15.py`
- **new**: `polars.expr.expr.Expr.map/Vi_py-0.19.0.py`
- **+2 / -3**

```diff
--- polars.expr.expr.Expr.map/Vi-1_py-0.18.15.py
+++ polars.expr.expr.Expr.map/Vi_py-0.19.0.py
@@ -1,3 +1,4 @@
+    @deprecate_renamed_function("map_batches", version="0.19.0")
     def map(
         self,
         function: Callable[[Series], Series | Any],
@@ -6,6 +7,4 @@
         agg_list: bool = False,
     ) -> Self:
         
-        if return_dtype is not None:
-            return_dtype = py_type_to_dtype(return_dtype)
-        return self._from_pyexpr(self._pyexpr.map(function, return_dtype, agg_list))
+        return self.map_batches(function, return_dtype, agg_list=agg_list)
```

```json
{
  "old_file": "polars.expr.expr.Expr.map/Vi-1_py-0.18.15.py",
  "new_file": "polars.expr.expr.Expr.map/Vi_py-0.19.0.py",
  "lines_added": 2,
  "lines_removed": 3
}
```
