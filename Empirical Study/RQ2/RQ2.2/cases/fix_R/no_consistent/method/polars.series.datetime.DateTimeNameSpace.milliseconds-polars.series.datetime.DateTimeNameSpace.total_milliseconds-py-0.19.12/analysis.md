# 一、突变情况分析

- **Total**: 430
- **替代API**: `polars.series.datetime.DateTimeNameSpace.total_milliseconds`
- **10% 阈值**: 43.0

## Vi-1 (py-0.19.12-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.7500 |
| treeBased | 1 | 0.9286 |

## Vi (py-0.19.13-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 89 | 0.7397 |
| tokenBased | 1 | 0.5294 |
| treeBased | 67 | 0.5652 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 89 | -88 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 67 | -66 | true |

```json
{
  "total": 430,
  "replacement_api": "polars.series.datetime.DateTimeNameSpace.total_milliseconds",
  "threshold_10pct": 43.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.75
    },
    "treeBased": {
      "rank": 1,
      "score": 0.928571
    }
  },
  "vi": {
    "mapBased": {
      "rank": 89,
      "score": 0.739726
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.529412
    },
    "treeBased": {
      "rank": 67,
      "score": 0.565217
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
      "vi_rank": 67,
      "delta": -66,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.series.datetime.DateTimeNameSpace.milliseconds/Vi-1_py-0.19.12.py`
- **new**: `polars.series.datetime.DateTimeNameSpace.milliseconds/Vi_py-0.19.13.py`
- **+2 / -0**

```diff
--- polars.series.datetime.DateTimeNameSpace.milliseconds/Vi-1_py-0.19.12.py
+++ polars.series.datetime.DateTimeNameSpace.milliseconds/Vi_py-0.19.13.py
@@ -1,2 +1,4 @@
+    @deprecate_renamed_function("total_milliseconds", version="0.19.13")
     def milliseconds(self) -> Series:
         
+        return self.total_milliseconds()
```

```json
{
  "old_file": "polars.series.datetime.DateTimeNameSpace.milliseconds/Vi-1_py-0.19.12.py",
  "new_file": "polars.series.datetime.DateTimeNameSpace.milliseconds/Vi_py-0.19.13.py",
  "lines_added": 2,
  "lines_removed": 0
}
```
