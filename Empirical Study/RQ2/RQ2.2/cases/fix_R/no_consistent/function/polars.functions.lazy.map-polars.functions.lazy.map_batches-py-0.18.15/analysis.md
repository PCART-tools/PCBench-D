# 一、突变情况分析

- **Total**: 83
- **替代API**: `polars.functions.lazy.map_batches`
- **10% 阈值**: 8.3

## Vi-1 (py-0.18.15-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9978 |
| tokenBased | 1 | 0.9367 |
| treeBased | 1 | 0.9681 |

## Vi (py-0.19.0-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 14 | 0.7953 |
| tokenBased | 1 | 0.7750 |
| treeBased | 1 | 0.7931 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 14 | -13 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 1 | +0 | false |

```json
{
  "total": 83,
  "replacement_api": "polars.functions.lazy.map_batches",
  "threshold_10pct": 8.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.997756
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.936709
    },
    "treeBased": {
      "rank": 1,
      "score": 0.968085
    }
  },
  "vi": {
    "mapBased": {
      "rank": 14,
      "score": 0.795252
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.775
    },
    "treeBased": {
      "rank": 1,
      "score": 0.793103
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 14,
      "delta": -13,
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
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.functions.lazy.map/Vi-1_py-0.18.15.py`
- **new**: `polars.functions.lazy.map/Vi_py-0.19.0.py`
- **+2 / -6**

```diff
--- polars.functions.lazy.map/Vi-1_py-0.18.15.py
+++ polars.functions.lazy.map/Vi_py-0.19.0.py
@@ -1,12 +1,8 @@
+@deprecate_renamed_function("map_batches", version="0.19.0")
 def map(
     exprs: Sequence[str] | Sequence[Expr],
     function: Callable[[Sequence[Series]], Series],
     return_dtype: PolarsDataType | None = None,
 ) -> Expr:
     
-    exprs = parse_as_list_of_expressions(exprs)
-    return wrap_expr(
-        plr.map_mul(
-            exprs, function, return_dtype, apply_groups=False, returns_scalar=False
-        )
-    )
+    return map_batches(exprs, function, return_dtype)
```

```json
{
  "old_file": "polars.functions.lazy.map/Vi-1_py-0.18.15.py",
  "new_file": "polars.functions.lazy.map/Vi_py-0.19.0.py",
  "lines_added": 2,
  "lines_removed": 6
}
```
