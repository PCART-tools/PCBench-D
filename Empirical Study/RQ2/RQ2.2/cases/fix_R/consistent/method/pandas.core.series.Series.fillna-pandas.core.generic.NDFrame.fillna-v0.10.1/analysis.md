# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 123.1

## Vi-1 (v0.10.1-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 142 | 0.3607 |
| tokenBased | 292 | 0.3579 |
| treeBased | 160 | 0.4295 |

## Vi (v0.11.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 351 | 0.3267 |
| tokenBased | 355 | 0.3278 |
| treeBased | 273 | 0.4113 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 142 | 351 | -209 | true |
| tokenBased | 292 | 355 | -63 | false |
| treeBased | 160 | 273 | -113 | false |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 142,
      "score": 0.3607
    },
    "tokenBased": {
      "rank": 292,
      "score": 0.35786
    },
    "treeBased": {
      "rank": 160,
      "score": 0.429474
    }
  },
  "vi": {
    "mapBased": {
      "rank": 351,
      "score": 0.326671
    },
    "tokenBased": {
      "rank": 355,
      "score": 0.327759
    },
    "treeBased": {
      "rank": 273,
      "score": 0.411255
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 142,
      "vi_rank": 351,
      "delta": -209,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 292,
      "vi_rank": 355,
      "delta": -63,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 160,
      "vi_rank": 273,
      "delta": -113,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.series.Series.fillna/Vi-1_v0.10.1.py`
- **new**: `pandas.core.series.Series.fillna/Vi_v0.11.0.py`
- **+2 / -9**

```diff
--- pandas.core.series.Series.fillna/Vi-1_v0.10.1.py
+++ pandas.core.series.Series.fillna/Vi_v0.11.0.py
@@ -2,13 +2,8 @@
     def fillna(self, value=None, method=None, inplace=False,
                limit=None):
         
-        if inplace:
-            import warnings
-            warnings.warn("Series.fillna with inplace=True  will return None"
-                          " from pandas 0.11 onward", FutureWarning)
-
         if not self._can_hold_na:
-            return self.copy() if not inplace else self
+            return self.copy() if not inplace else None
 
         if value is not None:
             if method is not None:
@@ -34,7 +29,5 @@
             else:
                 result = Series(values, index=self.index, name=self.name)
 
-        if inplace:
-            return self
-        else:
+        if not inplace:
             return result
```

```json
{
  "old_file": "pandas.core.series.Series.fillna/Vi-1_v0.10.1.py",
  "new_file": "pandas.core.series.Series.fillna/Vi_v0.11.0.py",
  "lines_added": 2,
  "lines_removed": 9
}
```
