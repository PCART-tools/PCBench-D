# 一、突变情况分析

- **Total**: 430
- **替代API**: `polars.series.series.Series.scatter`
- **10% 阈值**: 43.0

## Vi-1 (py-0.19.13-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.6388 |
| tokenBased | 1 | 0.4866 |
| treeBased | 1 | 0.5516 |

## Vi (py-0.19.14-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 417 | 0.3697 |
| tokenBased | 33 | 0.2452 |
| treeBased | 2 | 0.4365 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 417 | -416 | true |
| tokenBased | 1 | 33 | -32 | false |
| treeBased | 1 | 2 | -1 | false |

```json
{
  "total": 430,
  "replacement_api": "polars.series.series.Series.scatter",
  "threshold_10pct": 43.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.638798
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.486631
    },
    "treeBased": {
      "rank": 1,
      "score": 0.551587
    }
  },
  "vi": {
    "mapBased": {
      "rank": 417,
      "score": 0.369741
    },
    "tokenBased": {
      "rank": 33,
      "score": 0.245161
    },
    "treeBased": {
      "rank": 2,
      "score": 0.436464
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 417,
      "delta": -416,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 33,
      "delta": -32,
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

- **old**: `polars.series.series.Series.set_at_idx/Vi-1_py-0.19.13.py`
- **new**: `polars.series.series.Series.set_at_idx/Vi_py-0.19.14.py`
- **+8 / -20**

```diff
--- polars.series.series.Series.set_at_idx/Vi-1_py-0.19.13.py
+++ polars.series.series.Series.set_at_idx/Vi_py-0.19.14.py
@@ -1,37 +1,25 @@
+    @deprecate_renamed_function("scatter", version="0.19.14")
+    @deprecate_renamed_parameter("idx", "indices", version="0.19.14")
+    @deprecate_renamed_parameter("value", "values", version="0.19.14")
     def set_at_idx(
         self,
-        idx: Series | np.ndarray[Any, Any] | Sequence[int] | int,
-        value: (
+        indices: Series | np.ndarray[Any, Any] | Sequence[int] | int,
+        values: (
             int
             | float
             | str
             | bool
+            | date
+            | datetime
             | Sequence[int]
             | Sequence[float]
             | Sequence[bool]
             | Sequence[str]
             | Sequence[date]
             | Sequence[datetime]
-            | date
-            | datetime
             | Series
             | None
         ),
     ) -> Series:
         
-        if isinstance(idx, int):
-            idx = [idx]
-        if len(idx) == 0:
-            return self
-
-        idx = Series("", idx)
-        if isinstance(value, (int, float, bool, str)) or (value is None):
-            value = Series("", [value])
-
-
-            if len(idx) > 0:
-                value = value.extend_constant(value[0], len(idx) - 1)
-        elif not isinstance(value, Series):
-            value = Series("", value)
-        self._s.set_at_idx(idx._s, value._s)
-        return self
+        return self.scatter(indices, values)
```

```json
{
  "old_file": "polars.series.series.Series.set_at_idx/Vi-1_py-0.19.13.py",
  "new_file": "polars.series.series.Series.set_at_idx/Vi_py-0.19.14.py",
  "lines_added": 8,
  "lines_removed": 20
}
```
