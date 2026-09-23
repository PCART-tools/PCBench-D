# 一、突变情况分析

- **Total**: 2901
- **替代API**: `pandas.core.series.Series.sort_index`
- **10% 阈值**: 290.1

## Vi-1 (v0.16.3-v0.24.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2672 | 0.2972 |
| tokenBased | 1116 | 0.3137 |
| treeBased | 1599 | 0.3694 |

## Vi (v0.17.0-v0.24.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2670 | 0.1957 |
| tokenBased | 2531 | 0.1053 |
| treeBased | 2553 | 0.2158 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2672 | 2670 | +2 | false |
| tokenBased | 1116 | 2531 | -1415 | true |
| treeBased | 1599 | 2553 | -954 | true |

```json
{
  "total": 2901,
  "replacement_api": "pandas.core.series.Series.sort_index",
  "threshold_10pct": 290.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2672,
      "score": 0.29717
    },
    "tokenBased": {
      "rank": 1116,
      "score": 0.313725
    },
    "treeBased": {
      "rank": 1599,
      "score": 0.369369
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2670,
      "score": 0.195732
    },
    "tokenBased": {
      "rank": 2531,
      "score": 0.105263
    },
    "treeBased": {
      "rank": 2553,
      "score": 0.215789
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2672,
      "vi_rank": 2670,
      "delta": 2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1116,
      "vi_rank": 2531,
      "delta": -1415,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1599,
      "vi_rank": 2553,
      "delta": -954,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.series.Series.sortlevel/Vi-1_v0.16.3.py`
- **new**: `pandas.core.series.Series.sortlevel/Vi_v0.17.0.py`
- **+1 / -8**

```diff
--- pandas.core.series.Series.sortlevel/Vi-1_v0.16.3.py
+++ pandas.core.series.Series.sortlevel/Vi_v0.17.0.py
@@ -1,10 +1,3 @@
     def sortlevel(self, level=0, ascending=True, sort_remaining=True):
         
-        if not isinstance(self.index, MultiIndex):
-            raise TypeError('can only sort by level with a hierarchical index')
-
-        new_index, indexer = self.index.sortlevel(level, ascending=ascending,
-                                                 sort_remaining=sort_remaining)
-        new_values = self.values.take(indexer)
-        return self._constructor(new_values,
-                                 index=new_index).__finalize__(self)
+        return self.sort_index(level=level, ascending=ascending, sort_remaining=sort_remaining)
```

```json
{
  "old_file": "pandas.core.series.Series.sortlevel/Vi-1_v0.16.3.py",
  "new_file": "pandas.core.series.Series.sortlevel/Vi_v0.17.0.py",
  "lines_added": 1,
  "lines_removed": 8
}
```
