# 一、突变情况分析

- **Total**: 496
- **替代API**: `polars.expr.expr.Expr.shift`
- **10% 阈值**: 49.6

## Vi-1 (py-0.19.11-py-0.20.31)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 224 | 0.6752 |
| tokenBased | 36 | 0.5125 |
| treeBased | 46 | 0.7079 |

## Vi (py-0.19.11-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 221 | 0.6733 |
| tokenBased | 34 | 0.4458 |
| treeBased | 122 | 0.6024 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 224 | 221 | +3 | false |
| tokenBased | 36 | 34 | +2 | false |
| treeBased | 46 | 122 | -76 | true |

```json
{
  "total": 496,
  "replacement_api": "polars.expr.expr.Expr.shift",
  "threshold_10pct": 49.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 224,
      "score": 0.675159
    },
    "tokenBased": {
      "rank": 36,
      "score": 0.5125
    },
    "treeBased": {
      "rank": 46,
      "score": 0.707865
    }
  },
  "vi": {
    "mapBased": {
      "rank": 221,
      "score": 0.673301
    },
    "tokenBased": {
      "rank": 34,
      "score": 0.445783
    },
    "treeBased": {
      "rank": 122,
      "score": 0.60241
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 224,
      "vi_rank": 221,
      "delta": 3,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 36,
      "vi_rank": 34,
      "delta": 2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 46,
      "vi_rank": 122,
      "delta": -76,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.20.31/polars.expr.expr.Expr.shift.py`
- **new**: `R_candidates/Vi_py-1.0.0/polars.expr.expr.Expr.shift.py`
- **+3 / -4**

```diff
--- R_candidates/Vi-1_py-0.20.31/polars.expr.expr.Expr.shift.py
+++ R_candidates/Vi_py-1.0.0/polars.expr.expr.Expr.shift.py
@@ -1,9 +1,8 @@
-    @deprecate_renamed_parameter("periods", "n", version="0.19.11")
     def shift(
         self, n: int | IntoExprColumn = 1, *, fill_value: IntoExpr | None = None
-    ) -> Self:
+    ) -> Expr:
         
         if fill_value is not None:
-            fill_value = parse_as_expression(fill_value, str_as_lit=True)
-        n = parse_as_expression(n)
+            fill_value = parse_into_expression(fill_value, str_as_lit=True)
+        n = parse_into_expression(n)
         return self._from_pyexpr(self._pyexpr.shift(n, fill_value))
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.20.31/polars.expr.expr.Expr.shift.py",
  "new_file": "R_candidates/Vi_py-1.0.0/polars.expr.expr.Expr.shift.py",
  "lines_added": 3,
  "lines_removed": 4
}
```
