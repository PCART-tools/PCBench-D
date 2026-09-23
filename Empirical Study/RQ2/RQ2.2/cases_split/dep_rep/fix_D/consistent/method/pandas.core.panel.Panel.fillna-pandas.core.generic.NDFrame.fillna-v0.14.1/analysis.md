# 一、突变情况分析

- **Total**: 1280
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 128.0

## Vi-1 (v0.12.0-v0.14.1)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 637 | 0.3164 |
| tokenBased | 453 | 0.3061 |
| treeBased | 434 | 0.3950 |

## Vi (v0.12.0-v0.15.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 844 | 0.2878 |
| tokenBased | 557 | 0.2624 |
| treeBased | 622 | 0.3523 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 637 | 844 | -207 | true |
| tokenBased | 453 | 557 | -104 | false |
| treeBased | 434 | 622 | -188 | true |

```json
{
  "total": 1280,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 128.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 637,
      "score": 0.316448
    },
    "tokenBased": {
      "rank": 453,
      "score": 0.306122
    },
    "treeBased": {
      "rank": 434,
      "score": 0.394977
    }
  },
  "vi": {
    "mapBased": {
      "rank": 844,
      "score": 0.287779
    },
    "tokenBased": {
      "rank": 557,
      "score": 0.262391
    },
    "treeBased": {
      "rank": 622,
      "score": 0.352342
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 637,
      "vi_rank": 844,
      "delta": -207,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 453,
      "vi_rank": 557,
      "delta": -104,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 434,
      "vi_rank": 622,
      "delta": -188,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v0.14.1/pandas.core.generic.NDFrame.fillna.py`
- **new**: `R_candidates/Vi_v0.15.0/pandas.core.generic.NDFrame.fillna.py`
- **+11 / -2**

```diff
--- R_candidates/Vi-1_v0.14.1/pandas.core.generic.NDFrame.fillna.py
+++ R_candidates/Vi_v0.15.0/pandas.core.generic.NDFrame.fillna.py
@@ -9,6 +9,7 @@
         axis = self._get_axis_number(axis)
         method = com._clean_fill_method(method)
 
+        from pandas import DataFrame
         if value is None:
             if method is None:
                 raise ValueError('must specify a fill method or value')
@@ -51,10 +52,14 @@
             if len(self._get_axis(axis)) == 0:
                 return self
 
-            if self.ndim == 1 and value is not None:
+            if self.ndim == 1:
                 if isinstance(value, (dict, com.ABCSeries)):
                     from pandas import Series
                     value = Series(value)
+                elif not com.is_list_like(value):
+                    pass
+                else:
+                    raise ValueError("invalid fill value with a %s" % type(value))
 
                 new_data = self._data.fillna(value=value,
                                              limit=limit,
@@ -74,11 +79,15 @@
                     obj = result[k]
                     obj.fillna(v, limit=limit, inplace=True)
                 return result
-            else:
+            elif not com.is_list_like(value):
                 new_data = self._data.fillna(value=value,
                                              limit=limit,
                                              inplace=inplace,
                                              downcast=downcast)
+            elif isinstance(value, DataFrame) and self.ndim == 2:
+                new_data = self.where(self.notnull(), value)
+            else:
+                raise ValueError("invalid fill value with a %s" % type(value))
 
         if inplace:
             self._update_inplace(new_data)
```

```json
{
  "old_file": "R_candidates/Vi-1_v0.14.1/pandas.core.generic.NDFrame.fillna.py",
  "new_file": "R_candidates/Vi_v0.15.0/pandas.core.generic.NDFrame.fillna.py",
  "lines_added": 11,
  "lines_removed": 2
}
```
