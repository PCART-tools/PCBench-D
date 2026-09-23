# 一、突变情况分析

- **Total**: 1250
- **替代API**: `pandas.core.generic.NDFrame.take`
- **10% 阈值**: 125.0

## Vi-1 (v0.12.0-v0.13.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 1 | 0.5830 |
| tokenBased | 1 | 0.7222 |
| treeBased | 1 | 0.6255 |

## Vi (v0.12.0-v0.14.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 284 | 0.3538 |
| tokenBased | 272 | 0.3852 |
| treeBased | 158 | 0.4516 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 1 | 284 | -283 | true |
| tokenBased | 1 | 272 | -271 | true |
| treeBased | 1 | 158 | -157 | true |

```json
{
  "total": 1250,
  "replacement_api": "pandas.core.generic.NDFrame.take",
  "threshold_10pct": 125.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 1,
      "score": 0.582984
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.722222
    },
    "treeBased": {
      "rank": 1,
      "score": 0.625532
    }
  },
  "vi": {
    "mapBased": {
      "rank": 284,
      "score": 0.353793
    },
    "tokenBased": {
      "rank": 272,
      "score": 0.385246
    },
    "treeBased": {
      "rank": 158,
      "score": 0.451613
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 1,
      "vi_rank": 284,
      "delta": -283,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 272,
      "delta": -271,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 158,
      "delta": -157,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.13.1/pandas.core.generic.NDFrame.take.py`
- **new**: `R_candidates/Vi_v0.14.0/pandas.core.generic.NDFrame.take.py`
- **+3 / -15**

```diff
--- R_candidates/Vi-1_v0.13.1/pandas.core.generic.NDFrame.take.py
+++ R_candidates/Vi_v0.14.0/pandas.core.generic.NDFrame.take.py
@@ -1,21 +1,9 @@
     def take(self, indices, axis=0, convert=True, is_copy=True):
         
 
-
-        if convert:
-            axis = self._get_axis_number(axis)
-            indices = _maybe_convert_indices(
-                indices, len(self._get_axis(axis)))
-
-        baxis = self._get_block_manager_axis(axis)
-        if baxis == 0:
-            labels = self._get_axis(axis)
-            new_items = labels.take(indices)
-            new_data = self._data.reindex_axis(new_items, indexer=indices,
-                                               axis=baxis)
-        else:
-            new_data = self._data.take(indices, axis=baxis)
-
+        new_data = self._data.take(indices,
+                                   axis=self._get_block_manager_axis(axis),
+                                   convert=True, verify=True)
         result = self._constructor(new_data).__finalize__(self)
 
 
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.13.1/pandas.core.generic.NDFrame.take.py",
  "new_file": "R_candidates/Vi_v0.14.0/pandas.core.generic.NDFrame.take.py",
  "lines_added": 3,
  "lines_removed": 15
}
```
