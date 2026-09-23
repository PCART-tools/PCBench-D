# 一、突变情况分析

- **Total**: 146
- **替代API**: `dask.array.core.Array.to_delayed`
- **10% 阈值**: 14.6

## Vi-1 (0.8.2-0.14.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.6571 |
| treeBased | 1 | 0.8596 |

## Vi (0.8.2-0.15.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 91 | 0.6084 |
| tokenBased | 1 | 0.4894 |
| treeBased | 2 | 0.5797 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 91 | -90 | true |
| tokenBased | 1 | 1 | +0 | false |
| treeBased | 1 | 2 | -1 | false |

```json
{
  "total": 146,
  "replacement_api": "dask.array.core.Array.to_delayed",
  "threshold_10pct": 14.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.657143
    },
    "treeBased": {
      "rank": 1,
      "score": 0.859649
    }
  },
  "vi": {
    "mapBased": {
      "rank": 91,
      "score": 0.608434
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.489362
    },
    "treeBased": {
      "rank": 2,
      "score": 0.57971
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 91,
      "delta": -90,
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
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_0.14.3/dask.array.core.Array.to_delayed.py`
- **new**: `R_candidates/Vi_0.15.0/dask.array.core.Array.to_delayed.py`
- **+3 / -2**

```diff
--- R_candidates/Vi-1_0.14.3/dask.array.core.Array.to_delayed.py
+++ R_candidates/Vi_0.15.0/dask.array.core.Array.to_delayed.py
@@ -1,5 +1,6 @@
     def to_delayed(self):
         
         from ..delayed import Delayed
-        return np.array(ndeepmap(self.ndim, lambda k: Delayed(k, self.dask), self._keys()),
-                        dtype=object)
+        dsk = self._optimize(self.dask, self._keys())
+        L = ndeepmap(self.ndim, lambda k: Delayed(k, dsk), self._keys())
+        return np.array(L, dtype=object)
```

```json
{
  "old_file": "R_candidates/Vi-1_0.14.3/dask.array.core.Array.to_delayed.py",
  "new_file": "R_candidates/Vi_0.15.0/dask.array.core.Array.to_delayed.py",
  "lines_added": 3,
  "lines_removed": 2
}
```
