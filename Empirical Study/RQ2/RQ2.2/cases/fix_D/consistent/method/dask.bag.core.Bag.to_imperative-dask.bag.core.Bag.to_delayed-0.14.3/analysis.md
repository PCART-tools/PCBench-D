# 一、突变情况分析

- **Total**: 52
- **替代API**: `dask.bag.core.Bag.to_delayed`
- **10% 阈值**: 5.2

## Vi-1 (0.8.2-0.14.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.6400 |
| treeBased | 1 | 0.8780 |

## Vi (0.8.2-0.15.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 20 | 0.7814 |
| tokenBased | 2 | 0.4706 |
| treeBased | 2 | 0.6400 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 20 | -19 | true |
| tokenBased | 1 | 2 | -1 | false |
| treeBased | 1 | 2 | -1 | false |

```json
{
  "total": 52,
  "replacement_api": "dask.bag.core.Bag.to_delayed",
  "threshold_10pct": 5.2,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.64
    },
    "treeBased": {
      "rank": 1,
      "score": 0.878049
    }
  },
  "vi": {
    "mapBased": {
      "rank": 20,
      "score": 0.781362
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.470588
    },
    "treeBased": {
      "rank": 2,
      "score": 0.64
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 20,
      "delta": -19,
      "exceeds_10pct": true
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
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.14.3/dask.bag.core.Bag.to_delayed.py`
- **new**: `R_candidates/Vi_0.15.0/dask.bag.core.Bag.to_delayed.py`
- **+2 / -1**

```diff
--- R_candidates/Vi-1_0.14.3/dask.bag.core.Bag.to_delayed.py
+++ R_candidates/Vi_0.15.0/dask.bag.core.Bag.to_delayed.py
@@ -1,4 +1,5 @@
     def to_delayed(self):
         
         from dask.delayed import Delayed
-        return [Delayed(k, self.dask) for k in self._keys()]
+        dsk = self._optimize(self.dask, self._keys())
+        return [Delayed(k, dsk) for k in self._keys()]
```

```json
{
  "old_file": "R_candidates/Vi-1_0.14.3/dask.bag.core.Bag.to_delayed.py",
  "new_file": "R_candidates/Vi_0.15.0/dask.bag.core.Bag.to_delayed.py",
  "lines_added": 2,
  "lines_removed": 1
}
```
