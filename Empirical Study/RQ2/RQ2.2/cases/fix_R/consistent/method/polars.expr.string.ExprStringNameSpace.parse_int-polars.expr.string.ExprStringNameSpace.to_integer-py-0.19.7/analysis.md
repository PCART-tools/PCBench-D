# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.string.ExprStringNameSpace.to_integer`
- **10% 阈值**: 45.7

## Vi-1 (py-0.19.7-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 101 | 0.7953 |
| tokenBased | 31 | 0.4219 |
| treeBased | 40 | 0.7719 |

## Vi (py-0.19.8-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 6 | 0.7845 |
| tokenBased | 4 | 0.5070 |
| treeBased | 3 | 0.7432 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 101 | 6 | +95 | true |
| tokenBased | 31 | 4 | +27 | false |
| treeBased | 40 | 3 | +37 | false |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.string.ExprStringNameSpace.to_integer",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 101,
      "score": 0.795252
    },
    "tokenBased": {
      "rank": 31,
      "score": 0.421875
    },
    "treeBased": {
      "rank": 40,
      "score": 0.77193
    }
  },
  "vi": {
    "mapBased": {
      "rank": 6,
      "score": 0.784515
    },
    "tokenBased": {
      "rank": 4,
      "score": 0.507042
    },
    "treeBased": {
      "rank": 3,
      "score": 0.743243
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 101,
      "vi_rank": 6,
      "delta": 95,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 31,
      "vi_rank": 4,
      "delta": 27,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 40,
      "vi_rank": 3,
      "delta": 37,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.string.ExprStringNameSpace.parse_int/Vi-1_py-0.19.7.py`
- **new**: `polars.expr.string.ExprStringNameSpace.parse_int/Vi_py-0.19.8.py`
- **+9 / -1**

```diff
--- polars.expr.string.ExprStringNameSpace.parse_int/Vi-1_py-0.19.7.py
+++ polars.expr.string.ExprStringNameSpace.parse_int/Vi_py-0.19.8.py
@@ -1,3 +1,11 @@
-    def parse_int(self, radix: int = 2, *, strict: bool = True) -> Expr:
+    def parse_int(self, radix: int | None = None, *, strict: bool = True) -> Expr:
         
+        if radix is None:
+            issue_deprecation_warning(
+                "The default value for the `radix` parameter of `parse_int` will be removed in a future version."
+                " Call `parse_int(radix=2)` to keep current behavior and silence this warning.",
+                version="0.19.8",
+            )
+            radix = 2
+
         return wrap_expr(self._pyexpr.str_parse_int(radix, strict))
```

```json
{
  "old_file": "polars.expr.string.ExprStringNameSpace.parse_int/Vi-1_py-0.19.7.py",
  "new_file": "polars.expr.string.ExprStringNameSpace.parse_int/Vi_py-0.19.8.py",
  "lines_added": 9,
  "lines_removed": 1
}
```
