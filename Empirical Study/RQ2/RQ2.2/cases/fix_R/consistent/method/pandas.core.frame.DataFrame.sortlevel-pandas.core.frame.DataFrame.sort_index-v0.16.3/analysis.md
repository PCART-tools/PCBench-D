# 一、突变情况分析

- **Total**: 2901
- **替代API**: `pandas.core.frame.DataFrame.sort_index`
- **10% 阈值**: 290.1

## Vi-1 (v0.16.3-v0.24.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 221 | 0.4556 |
| tokenBased | 74 | 0.5025 |
| treeBased | 7 | 0.5318 |

## Vi (v0.17.0-v0.24.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2626 | 0.2156 |
| tokenBased | 2605 | 0.1117 |
| treeBased | 2622 | 0.2360 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 221 | 2626 | -2405 | true |
| tokenBased | 74 | 2605 | -2531 | true |
| treeBased | 7 | 2622 | -2615 | true |

```json
{
  "total": 2901,
  "replacement_api": "pandas.core.frame.DataFrame.sort_index",
  "threshold_10pct": 290.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 221,
      "score": 0.455647
    },
    "tokenBased": {
      "rank": 74,
      "score": 0.502538
    },
    "treeBased": {
      "rank": 7,
      "score": 0.531792
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2626,
      "score": 0.215584
    },
    "tokenBased": {
      "rank": 2605,
      "score": 0.111702
    },
    "treeBased": {
      "rank": 2622,
      "score": 0.236
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 221,
      "vi_rank": 2626,
      "delta": -2405,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 74,
      "vi_rank": 2605,
      "delta": -2531,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 7,
      "vi_rank": 2622,
      "delta": -2615,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.frame.DataFrame.sortlevel/Vi-1_v0.16.3.py`
- **new**: `pandas.core.frame.DataFrame.sortlevel/Vi_v0.17.0.py`
- **+2 / -23**

```diff
--- pandas.core.frame.DataFrame.sortlevel/Vi-1_v0.16.3.py
+++ pandas.core.frame.DataFrame.sortlevel/Vi_v0.17.0.py
@@ -1,26 +1,5 @@
     def sortlevel(self, level=0, axis=0, ascending=True,
                   inplace=False, sort_remaining=True):
         
-        axis = self._get_axis_number(axis)
-        the_axis = self._get_axis(axis)
-        if not isinstance(the_axis, MultiIndex):
-            raise TypeError('can only sort by level with a hierarchical index')
-
-        new_axis, indexer = the_axis.sortlevel(level, ascending=ascending,
-                                               sort_remaining=sort_remaining)
-
-        if self._is_mixed_type and not inplace:
-            ax = 'index' if axis == 0 else 'columns'
-
-            if new_axis.is_unique:
-                return self.reindex(**{ax: new_axis})
-            else:
-                return self.take(indexer, axis=axis, convert=False)
-
-        bm_axis = self._get_block_manager_axis(axis)
-        new_data = self._data.take(indexer, axis=bm_axis,
-                                   convert=False, verify=False)
-        if inplace:
-            return self._update_inplace(new_data)
-        else:
-            return self._constructor(new_data).__finalize__(self)
+        return self.sort_index(level=level, axis=axis, ascending=ascending,
+                               inplace=inplace, sort_remaining=sort_remaining)
```

```json
{
  "old_file": "pandas.core.frame.DataFrame.sortlevel/Vi-1_v0.16.3.py",
  "new_file": "pandas.core.frame.DataFrame.sortlevel/Vi_v0.17.0.py",
  "lines_added": 2,
  "lines_removed": 23
}
```
