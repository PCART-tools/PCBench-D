# 一、突变情况分析

- **Total**: 439
- **替代API**: `polars.series.series.Series.gather_every`
- **10% 阈值**: 43.9

## Vi-1 (py-0.19.13-py-0.20.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 2 | 0.7000 |
| treeBased | 1 | 0.9444 |

## Vi (py-0.19.13-py-0.20.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 72 | 0.8931 |
| tokenBased | 2 | 0.5385 |
| treeBased | 134 | 0.7727 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 72 | -71 | true |
| tokenBased | 2 | 2 | +0 | false |
| treeBased | 1 | 134 | -133 | true |

```json
{
  "total": 439,
  "replacement_api": "polars.series.series.Series.gather_every",
  "threshold_10pct": 43.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.7
    },
    "treeBased": {
      "rank": 1,
      "score": 0.944444
    }
  },
  "vi": {
    "mapBased": {
      "rank": 72,
      "score": 0.893082
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.538462
    },
    "treeBased": {
      "rank": 134,
      "score": 0.772727
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 72,
      "delta": -71,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2,
      "vi_rank": 2,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 134,
      "delta": -133,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.20.2/polars.series.series.Series.gather_every.py`
- **new**: `R_candidates/Vi_py-0.20.3/polars.series.series.Series.gather_every.py`
- **+1 / -1**

```diff
--- R_candidates/Vi-1_py-0.20.2/polars.series.series.Series.gather_every.py
+++ R_candidates/Vi_py-0.20.3/polars.series.series.Series.gather_every.py
@@ -1,2 +1,2 @@
-    def gather_every(self, n: int) -> Series:
+    def gather_every(self, n: int, offset: int = 0) -> Series:
         
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.20.2/polars.series.series.Series.gather_every.py",
  "new_file": "R_candidates/Vi_py-0.20.3/polars.series.series.Series.gather_every.py",
  "lines_added": 1,
  "lines_removed": 1
}
```
