# 一、突变情况分析

- **Total**: 212
- **替代API**: `polars.dataframe.frame.DataFrame.group_by`
- **10% 阈值**: 21.2

## Vi-1 (py-0.18.15-py-1.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8103 |
| treeBased | 1 | 0.8246 |

## Vi (py-0.18.15-py-1.2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 48 | 0.7540 |
| tokenBased | 3 | 0.4947 |
| treeBased | 63 | 0.4896 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 48 | -47 | true |
| tokenBased | 1 | 3 | -2 | false |
| treeBased | 1 | 63 | -62 | true |

```json
{
  "total": 212,
  "replacement_api": "polars.dataframe.frame.DataFrame.group_by",
  "threshold_10pct": 21.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.810345
    },
    "treeBased": {
      "rank": 1,
      "score": 0.824561
    }
  },
  "vi": {
    "mapBased": {
      "rank": 48,
      "score": 0.75395
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.494737
    },
    "treeBased": {
      "rank": 63,
      "score": 0.489583
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 48,
      "delta": -47,
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
      "vi1_rank": 1,
      "vi_rank": 63,
      "delta": -62,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-1.1.0/polars.dataframe.frame.DataFrame.group_by.py`
- **new**: `R_candidates/Vi_py-1.2.0/polars.dataframe.frame.DataFrame.group_by.py`
- **+10 / -0**

```diff
--- R_candidates/Vi-1_py-1.1.0/polars.dataframe.frame.DataFrame.group_by.py
+++ R_candidates/Vi_py-1.2.0/polars.dataframe.frame.DataFrame.group_by.py
@@ -5,4 +5,14 @@
         **named_by: IntoExpr,
     ) -> GroupBy:
         
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
         return GroupBy(self, *by, **named_by, maintain_order=maintain_order)
```

```json
{
  "old_file": "R_candidates/Vi-1_py-1.1.0/polars.dataframe.frame.DataFrame.group_by.py",
  "new_file": "R_candidates/Vi_py-1.2.0/polars.dataframe.frame.DataFrame.group_by.py",
  "lines_added": 10,
  "lines_removed": 0
}
```
