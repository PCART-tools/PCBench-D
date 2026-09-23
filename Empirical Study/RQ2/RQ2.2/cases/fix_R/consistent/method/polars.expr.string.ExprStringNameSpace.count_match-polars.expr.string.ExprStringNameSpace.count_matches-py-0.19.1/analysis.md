# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.string.ExprStringNameSpace.count_matches`
- **10% 阈值**: 45.7

## Vi-1 (py-0.19.1-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 318 | 0.6987 |
| tokenBased | 61 | 0.4231 |
| treeBased | 298 | 0.6667 |

## Vi (py-0.19.2-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 62 | 0.9291 |
| tokenBased | 1 | 0.6792 |
| treeBased | 23 | 0.8596 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 318 | 62 | +256 | true |
| tokenBased | 61 | 1 | +60 | true |
| treeBased | 298 | 23 | +275 | true |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.string.ExprStringNameSpace.count_matches",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 318,
      "score": 0.698718
    },
    "tokenBased": {
      "rank": 61,
      "score": 0.423077
    },
    "treeBased": {
      "rank": 298,
      "score": 0.666667
    }
  },
  "vi": {
    "mapBased": {
      "rank": 62,
      "score": 0.92911
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.679245
    },
    "treeBased": {
      "rank": 23,
      "score": 0.859649
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 318,
      "vi_rank": 62,
      "delta": 256,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 61,
      "vi_rank": 1,
      "delta": 60,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 298,
      "vi_rank": 23,
      "delta": 275,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.string.ExprStringNameSpace.count_match/Vi-1_py-0.19.1.py`
- **new**: `polars.expr.string.ExprStringNameSpace.count_match/Vi_py-0.19.2.py`
- **+2 / -1**

```diff
--- polars.expr.string.ExprStringNameSpace.count_match/Vi-1_py-0.19.1.py
+++ polars.expr.string.ExprStringNameSpace.count_match/Vi_py-0.19.2.py
@@ -1,3 +1,4 @@
-    def count_match(self, pattern: str) -> Expr:
+    def count_match(self, pattern: str | Expr) -> Expr:
         
+        pattern = parse_as_expression(pattern, str_as_lit=True)
         return wrap_expr(self._pyexpr.str_count_match(pattern))
```

```json
{
  "old_file": "polars.expr.string.ExprStringNameSpace.count_match/Vi-1_py-0.19.1.py",
  "new_file": "polars.expr.string.ExprStringNameSpace.count_match/Vi_py-0.19.2.py",
  "lines_added": 2,
  "lines_removed": 1
}
```
