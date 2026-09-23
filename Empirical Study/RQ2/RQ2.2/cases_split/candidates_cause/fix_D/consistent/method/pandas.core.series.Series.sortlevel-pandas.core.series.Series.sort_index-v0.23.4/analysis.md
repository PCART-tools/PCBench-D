# 一、突变情况分析

- **Total**: 2609
- **替代API**: `pandas.core.series.Series.sort_index`
- **10% 阈值**: 260.9

## Vi-1 (v0.20.0-v0.23.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2418 | 0.2031 |
| tokenBased | 2301 | 0.1346 |
| treeBased | 2308 | 0.2513 |

## Vi (v0.20.0-v0.24.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2694 | 0.2068 |
| tokenBased | 2544 | 0.1364 |
| treeBased | 2571 | 0.2525 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2418 | 2694 | -276 | true |
| tokenBased | 2301 | 2544 | -243 | false |
| treeBased | 2308 | 2571 | -263 | true |

```json
{
  "total": 2609,
  "replacement_api": "pandas.core.series.Series.sort_index",
  "threshold_10pct": 260.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2418,
      "score": 0.20308
    },
    "tokenBased": {
      "rank": 2301,
      "score": 0.134615
    },
    "treeBased": {
      "rank": 2308,
      "score": 0.251256
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2694,
      "score": 0.206762
    },
    "tokenBased": {
      "rank": 2544,
      "score": 0.136364
    },
    "treeBased": {
      "rank": 2571,
      "score": 0.252525
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2418,
      "vi_rank": 2694,
      "delta": -276,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2301,
      "vi_rank": 2544,
      "delta": -243,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2308,
      "vi_rank": 2571,
      "delta": -263,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.23.4/pandas.core.series.Series.sort_index.py`
- **new**: `R_candidates/Vi_v0.24.0/pandas.core.series.Series.sort_index.py`
- **+4 / -3**

```diff
--- R_candidates/Vi-1_v0.23.4/pandas.core.series.Series.sort_index.py
+++ R_candidates/Vi_v0.24.0/pandas.core.series.Series.sort_index.py
@@ -4,7 +4,8 @@
 
 
         inplace = validate_bool_kwarg(inplace, 'inplace')
-        axis = self._get_axis_number(axis)
+
+        self._get_axis_number(axis)
         index = self.index
 
         if level is not None:
@@ -13,7 +14,7 @@
         elif isinstance(index, MultiIndex):
             from pandas.core.sorting import lexsort_indexer
             labels = index._sort_levels_monotonic()
-            indexer = lexsort_indexer(labels._get_labels_for_sorting(),
+            indexer = lexsort_indexer(labels._get_codes_for_sorting(),
                                       orders=ascending,
                                       na_position=na_position)
         else:
@@ -31,7 +32,7 @@
             indexer = nargsort(index, kind=kind, ascending=ascending,
                                na_position=na_position)
 
-        indexer = _ensure_platform_int(indexer)
+        indexer = ensure_platform_int(indexer)
         new_index = index.take(indexer)
         new_index = new_index._sort_levels_monotonic()
 
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.23.4/pandas.core.series.Series.sort_index.py",
  "new_file": "R_candidates/Vi_v0.24.0/pandas.core.series.Series.sort_index.py",
  "lines_added": 4,
  "lines_removed": 3
}
```
