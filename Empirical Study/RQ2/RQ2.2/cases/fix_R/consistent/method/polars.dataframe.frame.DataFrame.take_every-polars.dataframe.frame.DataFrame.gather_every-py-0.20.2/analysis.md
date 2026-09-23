# 一、突变情况分析

- **Total**: 211
- **替代API**: `polars.dataframe.frame.DataFrame.gather_every`
- **10% 阈值**: 21.1

## Vi-1 (py-0.20.2-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 26 | 0.9035 |
| tokenBased | 2 | 0.4884 |
| treeBased | 47 | 0.5909 |

## Vi (py-0.20.3-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.6512 |
| treeBased | 3 | 0.7347 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 26 | 1 | +25 | true |
| tokenBased | 2 | 1 | +1 | false |
| treeBased | 47 | 3 | +44 | true |

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
      "rank": 2,
      "score": 0.488372
    },
    "treeBased": {
      "rank": 47,
      "score": 0.590909
    }
  },
  "vi": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.651163
    },
    "treeBased": {
      "rank": 3,
      "score": 0.734694
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 26,
      "vi_rank": 1,
      "delta": 25,
      "exceeds_10pct": true
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
      "vi1_rank": 47,
      "vi_rank": 3,
      "delta": 44,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.dataframe.frame.DataFrame.take_every/Vi-1_py-0.20.2.py`
- **new**: `polars.dataframe.frame.DataFrame.take_every/Vi_py-0.20.3.py`
- **+2 / -2**

```diff
--- polars.dataframe.frame.DataFrame.take_every/Vi-1_py-0.20.2.py
+++ polars.dataframe.frame.DataFrame.take_every/Vi_py-0.20.3.py
@@ -1,4 +1,4 @@
     @deprecate_renamed_function("gather_every", version="0.19.12")
-    def take_every(self, n: int) -> DataFrame:
+    def take_every(self, n: int, offset: int = 0) -> DataFrame:
         
-        return self.gather_every(n)
+        return self.gather_every(n, offset)
```

```json
{
  "old_file": "polars.dataframe.frame.DataFrame.take_every/Vi-1_py-0.20.2.py",
  "new_file": "polars.dataframe.frame.DataFrame.take_every/Vi_py-0.20.3.py",
  "lines_added": 2,
  "lines_removed": 2
}
```
