# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.string.ExprStringNameSpace.json_decode`
- **10% 阈值**: 45.7

## Vi-1 (py-0.19.14-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9980 |
| tokenBased | 1 | 0.8182 |
| treeBased | 1 | 0.9231 |

## Vi (py-0.19.15-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 289 | 0.7342 |
| tokenBased | 1 | 0.6212 |
| treeBased | 3 | 0.6667 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 289 | -288 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 3 | -2 | false |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.string.ExprStringNameSpace.json_decode",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.998038
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.818182
    },
    "treeBased": {
      "rank": 1,
      "score": 0.923077
    }
  },
  "vi": {
    "mapBased": {
      "rank": 289,
      "score": 0.734247
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.621212
    },
    "treeBased": {
      "rank": 3,
      "score": 0.666667
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 289,
      "delta": -288,
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
      "vi_rank": 3,
      "delta": -2,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.string.ExprStringNameSpace.json_extract/Vi-1_py-0.19.14.py`
- **new**: `polars.expr.string.ExprStringNameSpace.json_extract/Vi_py-0.19.15.py`
- **+2 / -3**

```diff
--- polars.expr.string.ExprStringNameSpace.json_extract/Vi-1_py-0.19.14.py
+++ polars.expr.string.ExprStringNameSpace.json_extract/Vi_py-0.19.15.py
@@ -1,7 +1,6 @@
+    @deprecate_renamed_function("json_decode", version="0.19.12")
     def json_extract(
         self, dtype: PolarsDataType | None = None, infer_schema_length: int | None = 100
     ) -> Expr:
         
-        if dtype is not None:
-            dtype = py_type_to_dtype(dtype)
-        return wrap_expr(self._pyexpr.str_json_extract(dtype, infer_schema_length))
+        return self.json_decode(dtype, infer_schema_length)
```

```json
{
  "old_file": "polars.expr.string.ExprStringNameSpace.json_extract/Vi-1_py-0.19.14.py",
  "new_file": "polars.expr.string.ExprStringNameSpace.json_extract/Vi_py-0.19.15.py",
  "lines_added": 2,
  "lines_removed": 3
}
```
