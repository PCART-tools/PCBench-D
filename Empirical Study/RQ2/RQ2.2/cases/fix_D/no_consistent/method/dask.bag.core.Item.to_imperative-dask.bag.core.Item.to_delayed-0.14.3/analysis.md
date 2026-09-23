# 一、突变情况分析

- **Total**: 52
- **替代API**: `dask.bag.core.Item.to_delayed`
- **10% 阈值**: 5.2

## Vi-1 (0.8.2-0.14.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.5714 |
| treeBased | 1 | 0.8387 |

## Vi (0.8.2-0.15.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 21 | 0.7814 |
| tokenBased | 1 | 0.4643 |
| treeBased | 10 | 0.6250 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 21 | -20 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 10 | -9 | true |

```json
{
  "total": 52,
  "replacement_api": "dask.bag.core.Item.to_delayed",
  "threshold_10pct": 5.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.571429
    },
    "treeBased": {
      "rank": 1,
      "score": 0.83871
    }
  },
  "vi": {
    "mapBased": {
      "rank": 21,
      "score": 0.781362
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.464286
    },
    "treeBased": {
      "rank": 10,
      "score": 0.625
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 21,
      "delta": -20,
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
      "vi_rank": 10,
      "delta": -9,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.14.3/dask.bag.core.Item.to_delayed.py`
- **new**: `R_candidates/Vi_0.15.0/dask.bag.core.Item.to_delayed.py`
- **+2 / -1**

```diff
--- R_candidates/Vi-1_0.14.3/dask.bag.core.Item.to_delayed.py
+++ R_candidates/Vi_0.15.0/dask.bag.core.Item.to_delayed.py
@@ -1,4 +1,5 @@
     def to_delayed(self):
         
         from dask.delayed import Delayed
-        return Delayed(self.key, self.dask)
+        dsk = self._optimize(self.dask, [self.key])
+        return Delayed(self.key, dsk)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.14.3/dask.bag.core.Item.to_delayed.py",
  "new_file": "R_candidates/Vi_0.15.0/dask.bag.core.Item.to_delayed.py",
  "lines_added": 2,
  "lines_removed": 1
}
```
