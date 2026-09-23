# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.list.ExprListNameSpace.gather`
- **10% 阈值**: 45.7

## Vi-1 (py-0.19.13-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9984 |
| tokenBased | 1 | 0.8571 |
| treeBased | 1 | 0.9706 |

## Vi (py-0.19.14-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 375 | 0.6146 |
| tokenBased | 1 | 0.5211 |
| treeBased | 1 | 0.6957 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 375 | -374 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 1 | +0 | false |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.list.ExprListNameSpace.gather",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.998415
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.857143
    },
    "treeBased": {
      "rank": 1,
      "score": 0.970588
    }
  },
  "vi": {
    "mapBased": {
      "rank": 375,
      "score": 0.614634
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.521127
    },
    "treeBased": {
      "rank": 1,
      "score": 0.695652
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 375,
      "delta": -374,
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

- **old**: `polars.expr.list.ExprListNameSpace.take/Vi-1_py-0.19.13.py`
- **new**: `polars.expr.list.ExprListNameSpace.take/Vi_py-0.19.14.py`
- **+4 / -5**

```diff
--- polars.expr.list.ExprListNameSpace.take/Vi-1_py-0.19.13.py
+++ polars.expr.list.ExprListNameSpace.take/Vi_py-0.19.14.py
@@ -1,11 +1,10 @@
+    @deprecate_renamed_function("gather", version="0.19.14")
+    @deprecate_renamed_parameter("index", "indices", version="0.19.14")
     def take(
         self,
-        index: Expr | Series | list[int] | list[list[int]],
+        indices: Expr | Series | list[int] | list[list[int]],
         *,
         null_on_oob: bool = False,
     ) -> Expr:
         
-        if isinstance(index, list):
-            index = pl.Series(index)
-        index = parse_as_expression(index)
-        return wrap_expr(self._pyexpr.list_take(index, null_on_oob))
+        return self.gather(indices)
```

```json
{
  "old_file": "polars.expr.list.ExprListNameSpace.take/Vi-1_py-0.19.13.py",
  "new_file": "polars.expr.list.ExprListNameSpace.take/Vi_py-0.19.14.py",
  "lines_added": 4,
  "lines_removed": 5
}
```
