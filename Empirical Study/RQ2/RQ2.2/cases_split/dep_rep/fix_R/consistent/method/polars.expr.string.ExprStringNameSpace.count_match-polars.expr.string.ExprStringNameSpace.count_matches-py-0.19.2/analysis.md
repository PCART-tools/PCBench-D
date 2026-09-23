# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.string.ExprStringNameSpace.count_matches`
- **10% 阈值**: 45.7

## Vi-1 (py-0.19.2-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 62 | 0.9291 |
| tokenBased | 1 | 0.6792 |
| treeBased | 23 | 0.8596 |

## Vi (py-0.19.3-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 318 | 0.6987 |
| tokenBased | 3 | 0.4906 |
| treeBased | 60 | 0.6346 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 62 | 318 | -256 | true |
| tokenBased | 1 | 3 | -2 | false |
| treeBased | 23 | 60 | -37 | false |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.string.ExprStringNameSpace.count_matches",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 318,
      "score": 0.698718
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.490566
    },
    "treeBased": {
      "rank": 60,
      "score": 0.634615
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 62,
      "vi_rank": 318,
      "delta": -256,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 3,
      "delta": -2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 23,
      "vi_rank": 60,
      "delta": -37,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.string.ExprStringNameSpace.count_match/Vi-1_py-0.19.2.py`
- **new**: `polars.expr.string.ExprStringNameSpace.count_match/Vi_py-0.19.3.py`
- **+2 / -2**

```diff
--- polars.expr.string.ExprStringNameSpace.count_match/Vi-1_py-0.19.2.py
+++ polars.expr.string.ExprStringNameSpace.count_match/Vi_py-0.19.3.py
@@ -1,4 +1,4 @@
+    @deprecate_renamed_function("count_matches", version="0.19.3")
     def count_match(self, pattern: str | Expr) -> Expr:
         
-        pattern = parse_as_expression(pattern, str_as_lit=True)
-        return wrap_expr(self._pyexpr.str_count_match(pattern))
+        return self.count_matches(pattern)
```

```json
{
  "old_file": "polars.expr.string.ExprStringNameSpace.count_match/Vi-1_py-0.19.2.py",
  "new_file": "polars.expr.string.ExprStringNameSpace.count_match/Vi_py-0.19.3.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
