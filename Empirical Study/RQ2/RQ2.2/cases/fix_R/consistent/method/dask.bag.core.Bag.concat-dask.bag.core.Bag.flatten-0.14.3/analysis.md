# 一、突变情况分析

- **Total**: 57
- **替代API**: `dask.bag.core.Bag.flatten`
- **10% 阈值**: 5.7

## Vi-1 (0.14.3-0.15.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 1.0000 |
| tokenBased | 1 | 0.8868 |
| treeBased | 1 | 0.9900 |

## Vi (0.15.0-0.15.2)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 28 | 0.6544 |
| tokenBased | 35 | 0.1818 |
| treeBased | 38 | 0.3594 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 28 | -27 | true |
| tokenBased | 1 | 35 | -34 | true |
| treeBased | 1 | 38 | -37 | true |

```json
{
  "total": 57,
  "replacement_api": "dask.bag.core.Bag.flatten",
  "threshold_10pct": 5.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 1.0
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.886792
    },
    "treeBased": {
      "rank": 1,
      "score": 0.99
    }
  },
  "vi": {
    "mapBased": {
      "rank": 28,
      "score": 0.654412
    },
    "tokenBased": {
      "rank": 35,
      "score": 0.181818
    },
    "treeBased": {
      "rank": 38,
      "score": 0.359375
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 28,
      "delta": -27,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 35,
      "delta": -34,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 38,
      "delta": -37,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `dask.bag.core.Bag.concat/Vi-1_0.14.3.py`
- **new**: `dask.bag.core.Bag.concat/Vi_0.15.0.py`
- **+2 / -5**

```diff
--- dask.bag.core.Bag.concat/Vi-1_0.14.3.py
+++ dask.bag.core.Bag.concat/Vi_0.15.0.py
@@ -1,6 +1,3 @@
     def concat(self):
-        
-        name = 'concat-' + tokenize(self)
-        dsk = dict(((name, i), (list, (toolz.concat, (self.name, i))))
-                   for i in range(self.npartitions))
-        return type(self)(merge(self.dask, dsk), name, self.npartitions)
+        warn("Deprecated.  Use the .flatten method instead")
+        return self.flatten()
```

```json
{
  "old_file": "dask.bag.core.Bag.concat/Vi-1_0.14.3.py",
  "new_file": "dask.bag.core.Bag.concat/Vi_0.15.0.py",
  "lines_added": 2,
  "lines_removed": 5
}
```
