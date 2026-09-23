# 一、突变情况分析

- **Total**: 2609
- **替代API**: `pandas.core.frame.DataFrame.sort_index`
- **10% 阈值**: 260.9

## Vi-1 (v0.20.0-v0.23.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2373 | 0.2256 |
| tokenBased | 2248 | 0.1497 |
| treeBased | 2193 | 0.2930 |

## Vi (v0.20.0-v0.24.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2649 | 0.2256 |
| tokenBased | 2492 | 0.1489 |
| treeBased | 2452 | 0.2907 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2373 | 2649 | -276 | true |
| tokenBased | 2248 | 2492 | -244 | false |
| treeBased | 2193 | 2452 | -259 | false |

```json
{
  "total": 2609,
  "replacement_api": "pandas.core.frame.DataFrame.sort_index",
  "threshold_10pct": 260.9,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2373,
      "score": 0.225641
    },
    "tokenBased": {
      "rank": 2248,
      "score": 0.149733
    },
    "treeBased": {
      "rank": 2193,
      "score": 0.292969
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2649,
      "score": 0.225641
    },
    "tokenBased": {
      "rank": 2492,
      "score": 0.148936
    },
    "treeBased": {
      "rank": 2452,
      "score": 0.290698
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2373,
      "vi_rank": 2649,
      "delta": -276,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 2248,
      "vi_rank": 2492,
      "delta": -244,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 2193,
      "vi_rank": 2452,
      "delta": -259,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.23.4/pandas.core.frame.DataFrame.sort_index.py`
- **new**: `R_candidates/Vi_v0.24.0/pandas.core.frame.DataFrame.sort_index.py`
- **+3 / -2**

```diff
--- R_candidates/Vi-1_v0.23.4/pandas.core.frame.DataFrame.sort_index.py
+++ R_candidates/Vi_v0.24.0/pandas.core.frame.DataFrame.sort_index.py
@@ -1,4 +1,5 @@
-    @Appender(_shared_docs['sort_index'] % _shared_doc_kwargs)
+    @Substitution(**_shared_doc_kwargs)
+    @Appender(NDFrame.sort_index.__doc__)
     def sort_index(self, axis=0, level=None, ascending=True, inplace=False,
                    kind='quicksort', na_position='last', sort_remaining=True,
                    by=None):
@@ -31,7 +32,7 @@
         elif isinstance(labels, MultiIndex):
             from pandas.core.sorting import lexsort_indexer
 
-            indexer = lexsort_indexer(labels._get_labels_for_sorting(),
+            indexer = lexsort_indexer(labels._get_codes_for_sorting(),
                                       orders=ascending,
                                       na_position=na_position)
         else:
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.23.4/pandas.core.frame.DataFrame.sort_index.py",
  "new_file": "R_candidates/Vi_v0.24.0/pandas.core.frame.DataFrame.sort_index.py",
  "lines_added": 3,
  "lines_removed": 2
}
```
