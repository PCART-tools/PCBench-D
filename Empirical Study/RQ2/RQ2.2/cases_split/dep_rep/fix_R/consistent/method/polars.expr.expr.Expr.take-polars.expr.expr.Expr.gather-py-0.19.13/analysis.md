# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.expr.Expr.gather`
- **10% 阈值**: 45.7

## Vi-1 (py-0.19.13-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9980 |
| tokenBased | 1 | 0.7609 |
| treeBased | 1 | 0.9485 |

## Vi (py-0.19.14-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 362 | 0.6412 |
| tokenBased | 11 | 0.3297 |
| treeBased | 10 | 0.5686 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 362 | -361 | true |
| tokenBased | 1 | 11 | -10 | false |
| treeBased | 1 | 10 | -9 | false |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.expr.Expr.gather",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.998038
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.76087
    },
    "treeBased": {
      "rank": 1,
      "score": 0.948529
    }
  },
  "vi": {
    "mapBased": {
      "rank": 362,
      "score": 0.641176
    },
    "tokenBased": {
      "rank": 11,
      "score": 0.32967
    },
    "treeBased": {
      "rank": 10,
      "score": 0.568627
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 362,
      "delta": -361,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 11,
      "delta": -10,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 10,
      "delta": -9,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.expr.Expr.take/Vi-1_py-0.19.13.py`
- **new**: `polars.expr.expr.Expr.take/Vi_py-0.19.14.py`
- **+2 / -7**

```diff
--- polars.expr.expr.Expr.take/Vi-1_py-0.19.13.py
+++ polars.expr.expr.Expr.take/Vi_py-0.19.14.py
@@ -1,11 +1,6 @@
+    @deprecate_renamed_function("gather", version="0.19.14")
     def take(
         self, indices: int | list[int] | Expr | Series | np.ndarray[Any, Any]
     ) -> Self:
         
-        if isinstance(indices, list) or (
-            _check_for_numpy(indices) and isinstance(indices, np.ndarray)
-        ):
-            indices_lit = F.lit(pl.Series("", indices, dtype=UInt32))._pyexpr
-        else:
-            indices_lit = parse_as_expression(indices)
-        return self._from_pyexpr(self._pyexpr.take(indices_lit))
+        return self.gather(indices)
```

```json
{
  "old_file": "polars.expr.expr.Expr.take/Vi-1_py-0.19.13.py",
  "new_file": "polars.expr.expr.Expr.take/Vi_py-0.19.14.py",
  "lines_added": 2,
  "lines_removed": 7
}
```
