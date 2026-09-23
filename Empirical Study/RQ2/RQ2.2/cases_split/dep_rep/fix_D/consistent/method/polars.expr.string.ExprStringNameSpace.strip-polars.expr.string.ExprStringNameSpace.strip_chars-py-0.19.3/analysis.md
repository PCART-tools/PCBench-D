# 一、突变情况分析

- **Total**: 401
- **替代API**: `polars.expr.string.ExprStringNameSpace.strip_chars`
- **10% 阈值**: 40.1

## Vi-1 (py-0.19.2-py-0.19.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8438 |
| treeBased | 1 | 0.9524 |

## Vi (py-0.19.2-py-0.19.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 280 | 0.7596 |
| tokenBased | 25 | 0.4510 |
| treeBased | 22 | 0.7959 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 280 | -279 | true |
| tokenBased | 1 | 25 | -24 | false |
| treeBased | 1 | 22 | -21 | false |

```json
{
  "total": 401,
  "replacement_api": "polars.expr.string.ExprStringNameSpace.strip_chars",
  "threshold_10pct": 40.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.84375
    },
    "treeBased": {
      "rank": 1,
      "score": 0.952381
    }
  },
  "vi": {
    "mapBased": {
      "rank": 280,
      "score": 0.759582
    },
    "tokenBased": {
      "rank": 25,
      "score": 0.45098
    },
    "treeBased": {
      "rank": 22,
      "score": 0.795918
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 280,
      "delta": -279,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 25,
      "delta": -24,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 22,
      "delta": -21,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.19.3/polars.expr.string.ExprStringNameSpace.strip_chars.py`
- **new**: `R_candidates/Vi_py-0.19.4/polars.expr.string.ExprStringNameSpace.strip_chars.py`
- **+2 / -1**

```diff
--- R_candidates/Vi-1_py-0.19.3/polars.expr.string.ExprStringNameSpace.strip_chars.py
+++ R_candidates/Vi_py-0.19.4/polars.expr.string.ExprStringNameSpace.strip_chars.py
@@ -1,3 +1,4 @@
-    def strip_chars(self, characters: str | None = None) -> Expr:
+    def strip_chars(self, characters: IntoExprColumn | None = None) -> Expr:
         
+        characters = parse_as_expression(characters, str_as_lit=True)
         return wrap_expr(self._pyexpr.str_strip_chars(characters))
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.19.3/polars.expr.string.ExprStringNameSpace.strip_chars.py",
  "new_file": "R_candidates/Vi_py-0.19.4/polars.expr.string.ExprStringNameSpace.strip_chars.py",
  "lines_added": 2,
  "lines_removed": 1
}
```
