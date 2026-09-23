# 一、突变情况分析

- **Total**: 120
- **替代API**: `polars.lazyframe.frame.LazyFrame.rolling`
- **10% 阈值**: 12.0

## Vi-1 (py-0.19.8-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.9724 |
| tokenBased | 1 | 0.8194 |
| treeBased | 1 | 0.8796 |

## Vi (py-0.19.9-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 89 | 0.4350 |
| tokenBased | 1 | 0.5878 |
| treeBased | 2 | 0.6154 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 89 | -88 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 2 | -1 | false |

```json
{
  "total": 120,
  "replacement_api": "polars.lazyframe.frame.LazyFrame.rolling",
  "threshold_10pct": 12.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.972374
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.819355
    },
    "treeBased": {
      "rank": 1,
      "score": 0.879581
    }
  },
  "vi": {
    "mapBased": {
      "rank": 89,
      "score": 0.435006
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.587838
    },
    "treeBased": {
      "rank": 2,
      "score": 0.615385
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 89,
      "delta": -88,
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

- **old**: `polars.lazyframe.frame.LazyFrame.group_by_rolling/Vi-1_py-0.19.8.py`
- **new**: `polars.lazyframe.frame.LazyFrame.group_by_rolling/Vi_py-0.19.9.py`
- **+8 / -11**

```diff
--- polars.lazyframe.frame.LazyFrame.group_by_rolling/Vi-1_py-0.19.8.py
+++ polars.lazyframe.frame.LazyFrame.group_by_rolling/Vi_py-0.19.9.py
@@ -1,3 +1,4 @@
+    @deprecate_renamed_function("rolling", version="0.19.9")
     def group_by_rolling(
         self,
         index_column: IntoExpr,
@@ -9,15 +10,11 @@
         check_sorted: bool = True,
     ) -> LazyGroupBy:
         
-        index_column = parse_as_expression(index_column)
-        if offset is None:
-            offset = _negate_duration(_timedelta_to_pl_duration(period))
-
-        pyexprs_by = parse_as_list_of_expressions(by) if by is not None else []
-        period = _timedelta_to_pl_duration(period)
-        offset = _timedelta_to_pl_duration(offset)
-
-        lgb = self._ldf.group_by_rolling(
-            index_column, period, offset, closed, pyexprs_by, check_sorted
+        return self.rolling(
+            index_column,
+            period=period,
+            offset=offset,
+            closed=closed,
+            by=by,
+            check_sorted=check_sorted,
         )
-        return LazyGroupBy(lgb)
```

```json
{
  "old_file": "polars.lazyframe.frame.LazyFrame.group_by_rolling/Vi-1_py-0.19.8.py",
  "new_file": "polars.lazyframe.frame.LazyFrame.group_by_rolling/Vi_py-0.19.9.py",
  "lines_added": 8,
  "lines_removed": 11
}
```
