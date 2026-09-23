# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.expr.Expr.shift`
- **10% 阈值**: 45.7

## Vi-1 (py-0.19.11-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 221 | 0.6733 |
| tokenBased | 34 | 0.4458 |
| treeBased | 122 | 0.6024 |

## Vi (py-0.19.12-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 379 | 0.6029 |
| tokenBased | 27 | 0.3415 |
| treeBased | 171 | 0.4872 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 221 | 379 | -158 | true |
| tokenBased | 34 | 27 | +7 | false |
| treeBased | 122 | 171 | -49 | true |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.expr.Expr.shift",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 379,
      "score": 0.602871
    },
    "tokenBased": {
      "rank": 27,
      "score": 0.341463
    },
    "treeBased": {
      "rank": 171,
      "score": 0.487179
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 221,
      "vi_rank": 379,
      "delta": -158,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 34,
      "vi_rank": 27,
      "delta": 7,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 122,
      "vi_rank": 171,
      "delta": -49,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.expr.Expr.shift_and_fill/Vi-1_py-0.19.11.py`
- **new**: `polars.expr.expr.Expr.shift_and_fill/Vi_py-0.19.12.py`
- **+2 / -2**

```diff
--- polars.expr.expr.Expr.shift_and_fill/Vi-1_py-0.19.11.py
+++ polars.expr.expr.Expr.shift_and_fill/Vi_py-0.19.12.py
@@ -1,3 +1,4 @@
+    @deprecate_function("Use `shift` instead.", version="0.19.12")
     @deprecate_renamed_parameter("periods", "n", version="0.19.11")
     def shift_and_fill(
         self,
@@ -6,5 +7,4 @@
         n: int = 1,
     ) -> Self:
         
-        fill_value = parse_as_expression(fill_value, str_as_lit=True)
-        return self._from_pyexpr(self._pyexpr.shift_and_fill(n, fill_value))
+        return self.shift(n, fill_value=fill_value)
```

```json
{
  "old_file": "polars.expr.expr.Expr.shift_and_fill/Vi-1_py-0.19.11.py",
  "new_file": "polars.expr.expr.Expr.shift_and_fill/Vi_py-0.19.12.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
