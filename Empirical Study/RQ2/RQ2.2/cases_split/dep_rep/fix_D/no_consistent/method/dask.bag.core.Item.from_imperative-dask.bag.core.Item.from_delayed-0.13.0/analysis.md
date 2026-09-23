# 一、突变情况分析

- **Total**: 52
- **替代API**: `dask.bag.core.Item.from_delayed`
- **10% 阈值**: 5.2

## Vi-1 (0.8.2-0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.7778 |
| treeBased | 1 | 0.9048 |

## Vi (0.8.2-0.14.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 23 | 0.6762 |
| tokenBased | 1 | 0.4565 |
| treeBased | 3 | 0.6333 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 23 | -22 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 3 | -2 | false |

```json
{
  "total": 52,
  "replacement_api": "dask.bag.core.Item.from_delayed",
  "threshold_10pct": 5.2,
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
      "score": 0.904762
    }
  },
  "vi": {
    "mapBased": {
      "rank": 23,
      "score": 0.676218
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.456522
    },
    "treeBased": {
      "rank": 3,
      "score": 0.633333
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 23,
      "delta": -22,
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

- **old**: `R_candidates/Vi-1_0.13.0/dask.bag.core.Item.from_delayed.py`
- **new**: `R_candidates/Vi_0.14.0/dask.bag.core.Item.from_delayed.py`
- **+3 / -1**

```diff
--- R_candidates/Vi-1_0.13.0/dask.bag.core.Item.from_delayed.py
+++ R_candidates/Vi_0.14.0/dask.bag.core.Item.from_delayed.py
@@ -1,6 +1,8 @@
     @staticmethod
     def from_delayed(value):
         
-        from dask.delayed import Delayed
+        from dask.delayed import Delayed, delayed
+        if not isinstance(value, Delayed) and hasattr(value, 'key'):
+            value = delayed(value)
         assert isinstance(value, Delayed)
         return Item(value.dask, value.key)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.13.0/dask.bag.core.Item.from_delayed.py",
  "new_file": "R_candidates/Vi_0.14.0/dask.bag.core.Item.from_delayed.py",
  "lines_added": 3,
  "lines_removed": 1
}
```
