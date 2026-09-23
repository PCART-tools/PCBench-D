# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.list.ExprListNameSpace.count_matches`
- **10% 阈值**: 45.7

## Vi-1 (py-0.19.2-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9974 |
| tokenBased | 1 | 0.7619 |
| treeBased | 1 | 0.9375 |

## Vi (py-0.19.3-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 268 | 0.7596 |
| tokenBased | 1 | 0.5238 |
| treeBased | 41 | 0.6744 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 268 | -267 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 41 | -40 | false |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.list.ExprListNameSpace.count_matches",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.997426
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.761905
    },
    "treeBased": {
      "rank": 1,
      "score": 0.9375
    }
  },
  "vi": {
    "mapBased": {
      "rank": 268,
      "score": 0.759582
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.52381
    },
    "treeBased": {
      "rank": 41,
      "score": 0.674419
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 268,
      "delta": -267,
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
      "vi_rank": 41,
      "delta": -40,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.list.ExprListNameSpace.count_match/Vi-1_py-0.19.2.py`
- **new**: `polars.expr.list.ExprListNameSpace.count_match/Vi_py-0.19.3.py`
- **+2 / -2**

```diff
--- polars.expr.list.ExprListNameSpace.count_match/Vi-1_py-0.19.2.py
+++ polars.expr.list.ExprListNameSpace.count_match/Vi_py-0.19.3.py
@@ -1,4 +1,4 @@
+    @deprecate_renamed_function("count_matches", version="0.19.3")
     def count_match(self, element: IntoExpr) -> Expr:
         
-        element = parse_as_expression(element, str_as_lit=True)
-        return wrap_expr(self._pyexpr.list_count_match(element))
+        return self.count_matches(element)
```

```json
{
  "old_file": "polars.expr.list.ExprListNameSpace.count_match/Vi-1_py-0.19.2.py",
  "new_file": "polars.expr.list.ExprListNameSpace.count_match/Vi_py-0.19.3.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
