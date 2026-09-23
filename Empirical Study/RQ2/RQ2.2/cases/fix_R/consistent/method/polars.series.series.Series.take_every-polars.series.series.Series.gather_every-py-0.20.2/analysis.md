# 一、突变情况分析

- **Total**: 430
- **替代API**: `polars.series.series.Series.gather_every`
- **10% 阈值**: 43.0

## Vi-1 (py-0.20.2-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 166 | 0.6927 |
| tokenBased | 3 | 0.4375 |
| treeBased | 150 | 0.5312 |

## Vi (py-0.20.3-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 81 | 0.7652 |
| tokenBased | 1 | 0.6061 |
| treeBased | 7 | 0.6757 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 166 | 81 | +85 | true |
| tokenBased | 3 | 1 | +2 | false |
| treeBased | 150 | 7 | +143 | true |

```json
{
  "total": 430,
  "replacement_api": "polars.series.series.Series.gather_every",
  "threshold_10pct": 43.0,
  "vi_minus_1": {
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
  "vi": {
    "mapBased": {
      "rank": 81,
      "score": 0.765217
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.606061
    },
    "treeBased": {
      "rank": 7,
      "score": 0.675676
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 166,
      "vi_rank": 81,
      "delta": 85,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 3,
      "vi_rank": 1,
      "delta": 2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 150,
      "vi_rank": 7,
      "delta": 143,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.series.series.Series.take_every/Vi-1_py-0.20.2.py`
- **new**: `polars.series.series.Series.take_every/Vi_py-0.20.3.py`
- **+2 / -2**

```diff
--- polars.series.series.Series.take_every/Vi-1_py-0.20.2.py
+++ polars.series.series.Series.take_every/Vi_py-0.20.3.py
@@ -1,4 +1,4 @@
     @deprecate_renamed_function("gather_every", version="0.19.14")
-    def take_every(self, n: int) -> Series:
+    def take_every(self, n: int, offset: int = 0) -> Series:
         
-        return self.gather_every(n)
+        return self.gather_every(n, offset)
```

```json
{
  "old_file": "polars.series.series.Series.take_every/Vi-1_py-0.20.2.py",
  "new_file": "polars.series.series.Series.take_every/Vi_py-0.20.3.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
