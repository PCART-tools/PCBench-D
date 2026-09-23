# 一、突变情况分析

- **Total**: 430
- **替代API**: `polars.series.series.Series.gather`
- **10% 阈值**: 43.0

## Vi-1 (py-0.19.13-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8378 |
| treeBased | 1 | 0.9792 |

## Vi (py-0.19.14-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 92 | 0.7553 |
| tokenBased | 1 | 0.7209 |
| treeBased | 1 | 0.8103 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 92 | -91 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 1 | +0 | false |

```json
{
  "total": 430,
  "replacement_api": "polars.series.series.Series.gather",
  "threshold_10pct": 43.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.837838
    },
    "treeBased": {
      "rank": 1,
      "score": 0.979167
    }
  },
  "vi": {
    "mapBased": {
      "rank": 92,
      "score": 0.755319
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.72093
    },
    "treeBased": {
      "rank": 1,
      "score": 0.810345
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 92,
      "delta": -91,
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
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.series.series.Series.take/Vi-1_py-0.19.13.py`
- **new**: `polars.series.series.Series.take/Vi_py-0.19.14.py`
- **+2 / -0**

```diff
--- polars.series.series.Series.take/Vi-1_py-0.19.13.py
+++ polars.series.series.Series.take/Vi_py-0.19.14.py
@@ -1,4 +1,6 @@
+    @deprecate_renamed_function("gather", version="0.19.14")
     def take(
         self, indices: int | list[int] | Expr | Series | np.ndarray[Any, Any]
     ) -> Series:
         
+        return self.gather(indices)
```

```json
{
  "old_file": "polars.series.series.Series.take/Vi-1_py-0.19.13.py",
  "new_file": "polars.series.series.Series.take/Vi_py-0.19.14.py",
  "lines_added": 2,
  "lines_removed": 0
}
```
