# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 123.1

## Vi-1 (v0.9.1-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 496 | 0.3065 |
| tokenBased | 471 | 0.2919 |
| treeBased | 477 | 0.3661 |

## Vi (v0.10.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 388 | 0.3215 |
| tokenBased | 354 | 0.3278 |
| treeBased | 290 | 0.4069 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 496 | 388 | +108 | false |
| tokenBased | 471 | 354 | +117 | false |
| treeBased | 477 | 290 | +187 | true |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 496,
      "score": 0.306463
    },
    "tokenBased": {
      "rank": 471,
      "score": 0.291946
    },
    "treeBased": {
      "rank": 477,
      "score": 0.366071
    }
  },
  "vi": {
    "mapBased": {
      "rank": 388,
      "score": 0.321517
    },
    "tokenBased": {
      "rank": 354,
      "score": 0.327759
    },
    "treeBased": {
      "rank": 290,
      "score": 0.406926
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 496,
      "vi_rank": 388,
      "delta": 108,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 471,
      "vi_rank": 354,
      "delta": 117,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 477,
      "vi_rank": 290,
      "delta": 187,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.series.Series.fillna/Vi-1_v0.9.1.py`
- **new**: `pandas.core.series.Series.fillna/Vi_v0.10.0.py`
- **+6 / -4**

```diff
--- pandas.core.series.Series.fillna/Vi-1_v0.9.1.py
+++ pandas.core.series.Series.fillna/Vi_v0.10.0.py
@@ -1,17 +1,19 @@
 
-    def fillna(self, value=None, method='pad', inplace=False,
+    def fillna(self, value=None, method=None, inplace=False,
                limit=None):
         
         if not self._can_hold_na:
-            return self.copy() if not inplace else self
+            return self.copy() if not inplace else None
 
         if value is not None:
+            if method is not None:
+                raise ValueError('Cannot specify both a fill value and method')
             result = self.copy() if not inplace else self
             mask = isnull(self.values)
             np.putmask(result, mask, value)
         else:
             if method is None:
-                raise ValueError('must specify a fill method')
+                raise ValueError('must specify a fill method or value')
 
             fill_f = _get_fill_func(method)
 
@@ -27,4 +29,4 @@
             else:
                 result = Series(values, index=self.index, name=self.name)
 
-        return result
+        return result if not inplace else None
```

```json
{
  "old_file": "pandas.core.series.Series.fillna/Vi-1_v0.9.1.py",
  "new_file": "pandas.core.series.Series.fillna/Vi_v0.10.0.py",
  "lines_added": 6,
  "lines_removed": 4
}
```
