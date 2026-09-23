# 一、突变情况分析

- **Total**: 1231
- **替代API**: `pandas.core.generic.NDFrame.fillna`
- **10% 阈值**: 123.1

## Vi-1 (v0.7.3-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 279 | 0.3476 |
| tokenBased | 331 | 0.3569 |
| treeBased | 442 | 0.3636 |

## Vi (v0.8.0-v0.13.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 632 | 0.2862 |
| tokenBased | 541 | 0.2712 |
| treeBased | 599 | 0.3448 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 279 | 632 | -353 | true |
| tokenBased | 331 | 541 | -210 | true |
| treeBased | 442 | 599 | -157 | true |

```json
{
  "total": 1231,
  "replacement_api": "pandas.core.generic.NDFrame.fillna",
  "threshold_10pct": 123.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 279,
      "score": 0.347625
    },
    "tokenBased": {
      "rank": 331,
      "score": 0.356902
    },
    "treeBased": {
      "rank": 442,
      "score": 0.363636
    }
  },
  "vi": {
    "mapBased": {
      "rank": 632,
      "score": 0.286196
    },
    "tokenBased": {
      "rank": 541,
      "score": 0.271186
    },
    "treeBased": {
      "rank": 599,
      "score": 0.344828
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 279,
      "vi_rank": 632,
      "delta": -353,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 331,
      "vi_rank": 541,
      "delta": -210,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 442,
      "vi_rank": 599,
      "delta": -157,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.series.Series.fillna/Vi-1_v0.7.3.py`
- **new**: `pandas.core.series.Series.fillna/Vi_v0.8.0.py`
- **+13 / -15**

```diff
--- pandas.core.series.Series.fillna/Vi-1_v0.7.3.py
+++ pandas.core.series.Series.fillna/Vi_v0.8.0.py
@@ -1,29 +1,27 @@
-    def fillna(self, value=None, method='pad', inplace=False):
+
+    def fillna(self, value=None, method='pad', inplace=False,
+               limit=None):
         
-        mask = isnull(self.values)
-
         if value is not None:
             result = self.copy() if not inplace else self
+            mask = isnull(self.values)
             np.putmask(result, mask, value)
         else:
             if method is None:
                 raise ValueError('must specify a fill method')
 
-            method = com._clean_fill_method(method)
-
-
-            mask = mask.astype(np.uint8)
-
-            if method == 'pad':
-                indexer = lib.get_pad_indexer(mask)
-            elif method == 'backfill':
-                indexer = lib.get_backfill_indexer(mask)
+            fill_f = _get_fill_func(method)
 
             if inplace:
-                self.values[:] = self.values.take(indexer)
+                values = self.values
+            else:
+                values = self.values.copy()
+
+            fill_f(values, limit=limit)
+
+            if inplace:
                 result = self
             else:
-                new_values = self.values.take(indexer)
-                result = Series(new_values, index=self.index, name=self.name)
+                result = Series(values, index=self.index, name=self.name)
 
         return result
```

```json
{
  "old_file": "pandas.core.series.Series.fillna/Vi-1_v0.7.3.py",
  "new_file": "pandas.core.series.Series.fillna/Vi_v0.8.0.py",
  "lines_added": 13,
  "lines_removed": 15
}
```
