# 一、突变情况分析

- **Total**: 225
- **替代API**: `polars.dataframe.frame.DataFrame.gather_every`
- **10% 阈值**: 22.5

## Vi-1 (py-0.19.13-py-0.20.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.7778 |
| treeBased | 1 | 0.9500 |

## Vi (py-0.19.13-py-0.20.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 30 | 0.9035 |
| tokenBased | 1 | 0.6512 |
| treeBased | 3 | 0.8444 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 30 | -29 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 3 | -2 | false |

```json
{
  "total": 225,
  "replacement_api": "polars.dataframe.frame.DataFrame.gather_every",
  "threshold_10pct": 22.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.777778
    },
    "treeBased": {
      "rank": 1,
      "score": 0.95
    }
  },
  "vi": {
    "mapBased": {
      "rank": 30,
      "score": 0.903475
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.651163
    },
    "treeBased": {
      "rank": 3,
      "score": 0.844444
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 30,
      "delta": -29,
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
      "vi_rank": 3,
      "delta": -2,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.20.2/polars.dataframe.frame.DataFrame.gather_every.py`
- **new**: `R_candidates/Vi_py-0.20.3/polars.dataframe.frame.DataFrame.gather_every.py`
- **+2 / -2**

```diff
--- R_candidates/Vi-1_py-0.20.2/polars.dataframe.frame.DataFrame.gather_every.py
+++ R_candidates/Vi_py-0.20.3/polars.dataframe.frame.DataFrame.gather_every.py
@@ -1,3 +1,3 @@
-    def gather_every(self, n: int) -> DataFrame:
+    def gather_every(self, n: int, offset: int = 0) -> DataFrame:
         
-        return self.select(F.col("*").gather_every(n))
+        return self.select(F.col("*").gather_every(n, offset))
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.20.2/polars.dataframe.frame.DataFrame.gather_every.py",
  "new_file": "R_candidates/Vi_py-0.20.3/polars.dataframe.frame.DataFrame.gather_every.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
