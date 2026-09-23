# 一、突变情况分析

- **Total**: 430
- **替代API**: `polars.series.series.Series.gather_every`
- **10% 阈值**: 43.0

## Vi-1 (py-0.19.13-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 71 | 0.8931 |
| tokenBased | 1 | 0.5385 |
| treeBased | 152 | 0.7727 |

## Vi (py-0.19.14-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 166 | 0.6927 |
| tokenBased | 3 | 0.4375 |
| treeBased | 150 | 0.5312 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 71 | 166 | -95 | true |
| tokenBased | 1 | 3 | -2 | false |
| treeBased | 152 | 150 | +2 | false |

```json
{
  "total": 430,
  "replacement_api": "polars.series.series.Series.gather_every",
  "threshold_10pct": 43.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 71,
      "score": 0.893082
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.538462
    },
    "treeBased": {
      "rank": 152,
      "score": 0.772727
    }
  },
  "vi": {
    "mapBased": {
      "rank": 166,
      "score": 0.692683
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.4375
    },
    "treeBased": {
      "rank": 150,
      "score": 0.53125
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 71,
      "vi_rank": 166,
      "delta": -95,
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
      "vi1_rank": 152,
      "vi_rank": 150,
      "delta": 2,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.series.series.Series.take_every/Vi-1_py-0.19.13.py`
- **new**: `polars.series.series.Series.take_every/Vi_py-0.19.14.py`
- **+2 / -0**

```diff
--- polars.series.series.Series.take_every/Vi-1_py-0.19.13.py
+++ polars.series.series.Series.take_every/Vi_py-0.19.14.py
@@ -1,2 +1,4 @@
+    @deprecate_renamed_function("gather_every", version="0.19.14")
     def take_every(self, n: int) -> Series:
         
+        return self.gather_every(n)
```

```json
{
  "old_file": "polars.series.series.Series.take_every/Vi-1_py-0.19.13.py",
  "new_file": "polars.series.series.Series.take_every/Vi_py-0.19.14.py",
  "lines_added": 2,
  "lines_removed": 0
}
```
