# 一、突变情况分析

- **Total**: 474
- **替代API**: `polars.series.series.Series.shift`
- **10% 阈值**: 47.4

## Vi-1 (py-0.19.11-py-0.20.31)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 2 | 0.6250 |
| treeBased | 4 | 0.7955 |

## Vi (py-0.19.11-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.6000 |
| treeBased | 55 | 0.6053 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 1 | +0 | false |
| tokenBased | 2 | 1 | +1 | false |
| treeBased | 4 | 55 | -51 | true |

```json
{
  "total": 474,
  "replacement_api": "polars.series.series.Series.shift",
  "threshold_10pct": 47.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.625
    },
    "treeBased": {
      "rank": 4,
      "score": 0.795455
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.6
    },
    "treeBased": {
      "rank": 55,
      "score": 0.605263
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 1,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 1,
      "delta": 1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 4,
      "vi_rank": 55,
      "delta": -51,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.20.31/polars.series.series.Series.shift.py`
- **new**: `R_candidates/Vi_py-1.0.0/polars.series.series.Series.shift.py`
- **+0 / -1**

```diff
--- R_candidates/Vi-1_py-0.20.31/polars.series.series.Series.shift.py
+++ R_candidates/Vi_py-1.0.0/polars.series.series.Series.shift.py
@@ -1,3 +1,2 @@
-    @deprecate_renamed_parameter("periods", "n", version="0.19.11")
     def shift(self, n: int = 1, *, fill_value: IntoExpr | None = None) -> Series:
         
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.20.31/polars.series.series.Series.shift.py",
  "new_file": "R_candidates/Vi_py-1.0.0/polars.series.series.Series.shift.py",
  "lines_added": 0,
  "lines_removed": 1
}
```
