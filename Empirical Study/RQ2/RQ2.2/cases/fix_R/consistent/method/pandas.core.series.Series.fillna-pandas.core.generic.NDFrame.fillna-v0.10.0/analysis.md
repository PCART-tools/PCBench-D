# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 123.1

## Vi-1 (v0.10.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 388 | 0.3215 |
| tokenBased | 354 | 0.3278 |
| treeBased | 290 | 0.4069 |

## Vi (v0.10.1-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 142 | 0.3607 |
| tokenBased | 292 | 0.3579 |
| treeBased | 160 | 0.4295 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 388 | 142 | +246 | true |
| tokenBased | 354 | 292 | +62 | false |
| treeBased | 290 | 160 | +130 | true |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
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
  "vi": {
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
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 388,
      "vi_rank": 142,
      "delta": 246,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 354,
      "vi_rank": 292,
      "delta": 62,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 290,
      "vi_rank": 160,
      "delta": 130,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.series.Series.fillna/Vi-1_v0.10.0.py`
- **new**: `pandas.core.series.Series.fillna/Vi_v0.10.1.py`
- **+10 / -2**

```diff
--- pandas.core.series.Series.fillna/Vi-1_v0.10.0.py
+++ pandas.core.series.Series.fillna/Vi_v0.10.1.py
@@ -2,8 +2,13 @@
     def fillna(self, value=None, method=None, inplace=False,
                limit=None):
         
+        if inplace:
+            import warnings
+            warnings.warn("Series.fillna with inplace=True  will return None"
+                          " from pandas 0.11 onward", FutureWarning)
+
         if not self._can_hold_na:
-            return self.copy() if not inplace else None
+            return self.copy() if not inplace else self
 
         if value is not None:
             if method is not None:
@@ -29,4 +34,7 @@
             else:
                 result = Series(values, index=self.index, name=self.name)
 
-        return result if not inplace else None
+        if inplace:
+            return self
+        else:
+            return result
```

```json
{
  "old_file": "pandas.core.series.Series.fillna/Vi-1_v0.10.0.py",
  "new_file": "pandas.core.series.Series.fillna/Vi_v0.10.1.py",
  "lines_added": 10,
  "lines_removed": 2
}
```
