# 一、突变情况分析

- **Total**: 211
- **替代API**: `polars.dataframe.frame.DataFrame.gather_every`
- **10% 阈值**: 21.1

## Vi-1 (py-0.19.13-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 26 | 0.9035 |
| tokenBased | 1 | 0.6512 |
| treeBased | 3 | 0.8444 |

## Vi (py-0.19.14-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 26 | 0.9035 |
| tokenBased | 2 | 0.4884 |
| treeBased | 47 | 0.5909 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 26 | 26 | +0 | false |
| tokenBased | 1 | 2 | -1 | false |
| treeBased | 3 | 47 | -44 | true |

```json
{
  "total": 211,
  "replacement_api": "polars.dataframe.frame.DataFrame.gather_every",
  "threshold_10pct": 21.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 26,
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
  "vi": {
    "mapBased": {
      "rank": 26,
      "score": 0.903475
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.488372
    },
    "treeBased": {
      "rank": 47,
      "score": 0.590909
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 26,
      "vi_rank": 26,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 3,
      "vi_rank": 47,
      "delta": -44,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.dataframe.frame.DataFrame.take_every/Vi-1_py-0.19.13.py`
- **new**: `polars.dataframe.frame.DataFrame.take_every/Vi_py-0.19.14.py`
- **+2 / -1**

```diff
--- polars.dataframe.frame.DataFrame.take_every/Vi-1_py-0.19.13.py
+++ polars.dataframe.frame.DataFrame.take_every/Vi_py-0.19.14.py
@@ -1,3 +1,4 @@
+    @deprecate_renamed_function("gather_every", version="0.19.12")
     def take_every(self, n: int) -> DataFrame:
         
-        return self.select(F.col("*").take_every(n))
+        return self.gather_every(n)
```

```json
{
  "old_file": "polars.dataframe.frame.DataFrame.take_every/Vi-1_py-0.19.13.py",
  "new_file": "polars.dataframe.frame.DataFrame.take_every/Vi_py-0.19.14.py",
  "lines_added": 2,
  "lines_removed": 1
}
```
