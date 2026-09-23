# 一、突变情况分析

- **Total**: 120
- **替代API**: `polars.lazyframe.frame.LazyFrame.group_by`
- **10% 阈值**: 12.0

## Vi-1 (py-0.18.15-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9382 |
| tokenBased | 1 | 0.7973 |
| treeBased | 1 | 0.8442 |

## Vi (py-0.19.0-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 64 | 0.6136 |
| tokenBased | 1 | 0.6575 |
| treeBased | 2 | 0.6250 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 64 | -63 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 2 | -1 | false |

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
      "rank": 64,
      "score": 0.613636
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.657534
    },
    "treeBased": {
      "rank": 2,
      "score": 0.625
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 64,
      "delta": -63,
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
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.lazyframe.frame.LazyFrame.groupby/Vi-1_py-0.18.15.py`
- **new**: `polars.lazyframe.frame.LazyFrame.groupby/Vi_py-0.19.0.py`
- **+2 / -3**

```diff
--- polars.lazyframe.frame.LazyFrame.groupby/Vi-1_py-0.18.15.py
+++ polars.lazyframe.frame.LazyFrame.groupby/Vi_py-0.19.0.py
@@ -1,3 +1,4 @@
+    @deprecate_renamed_function("group_by", version="0.19.0")
     def groupby(
         self,
         by: IntoExpr | Iterable[IntoExpr],
@@ -5,6 +6,4 @@
         maintain_order: bool = False,
     ) -> LazyGroupBy:
         
-        exprs = parse_as_list_of_expressions(by, *more_by)
-        lgb = self._ldf.groupby(exprs, maintain_order)
-        return LazyGroupBy(lgb)
+        return self.group_by(by, *more_by, maintain_order=maintain_order)
```

```json
{
  "old_file": "polars.lazyframe.frame.LazyFrame.groupby/Vi-1_py-0.18.15.py",
  "new_file": "polars.lazyframe.frame.LazyFrame.groupby/Vi_py-0.19.0.py",
  "lines_added": 2,
  "lines_removed": 3
}
```
