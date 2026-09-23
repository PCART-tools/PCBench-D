# 一、突变情况分析

- **Total**: 120
- **替代API**: `polars.lazyframe.frame.LazyFrame.group_by`
- **10% 阈值**: 12.0

## Vi-1 (py-0.18.15-py-1.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9382 |
| tokenBased | 1 | 0.7973 |
| treeBased | 1 | 0.8442 |

## Vi (py-0.18.15-py-1.2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 7 | 0.7821 |
| tokenBased | 5 | 0.5315 |
| treeBased | 20 | 0.5259 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 7 | -6 | false |
| tokenBased | 1 | 5 | -4 | false |
| treeBased | 1 | 20 | -19 | true |

```json
{
  "total": 120,
  "replacement_api": "polars.lazyframe.frame.LazyFrame.group_by",
  "threshold_10pct": 12.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.938187
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.797297
    },
    "treeBased": {
      "rank": 1,
      "score": 0.844156
    }
  },
  "vi": {
    "mapBased": {
      "rank": 7,
      "score": 0.782061
    },
    "tokenBased": {
      "rank": 5,
      "score": 0.531532
    },
    "treeBased": {
      "rank": 20,
      "score": 0.525862
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 7,
      "delta": -6,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 5,
      "delta": -4,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 20,
      "delta": -19,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-1.1.0/polars.lazyframe.frame.LazyFrame.group_by.py`
- **new**: `R_candidates/Vi_py-1.2.0/polars.lazyframe.frame.LazyFrame.group_by.py`
- **+10 / -0**

```diff
--- R_candidates/Vi-1_py-1.1.0/polars.lazyframe.frame.LazyFrame.group_by.py
+++ R_candidates/Vi_py-1.2.0/polars.lazyframe.frame.LazyFrame.group_by.py
@@ -5,6 +5,16 @@
         **named_by: IntoExpr,
     ) -> LazyGroupBy:
         
+        for _key, value in named_by.items():
+            if not isinstance(value, (str, pl.Expr, pl.Series)):
+                msg = (
+                    f"Expected Polars expression or object convertible to one, got {type(value)}.\n\n"
+                    "Hint: if you tried\n"
+                    f"    group_by(by={value!r})\n"
+                    "then you probably want to use this instead:\n"
+                    f"    group_by({value!r})"
+                )
+                raise TypeError(msg)
         exprs = parse_into_list_of_expressions(*by, **named_by)
         lgb = self._ldf.group_by(exprs, maintain_order)
         return LazyGroupBy(lgb)
```

```json
{
  "old_file": "R_candidates/Vi-1_py-1.1.0/polars.lazyframe.frame.LazyFrame.group_by.py",
  "new_file": "R_candidates/Vi_py-1.2.0/polars.lazyframe.frame.LazyFrame.group_by.py",
  "lines_added": 10,
  "lines_removed": 0
}
```
