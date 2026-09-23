# 一、突变情况分析

- **Total**: 58
- **替代API**: `sklearn.compose._column_transformer.ColumnTransformer.get_feature_names_out`
- **10% 阈值**: 5.8

## Vi-1 (0.22.2-1.2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.5420 |
| tokenBased | 1 | 0.5758 |
| treeBased | 4 | 0.5000 |

## Vi (0.23.0-1.2.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 2 | 0.4686 |
| tokenBased | 7 | 0.4000 |
| treeBased | 6 | 0.4174 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 2 | 2 | +0 | false |
| tokenBased | 1 | 7 | -6 | true |
| treeBased | 4 | 6 | -2 | false |

```json
{
  "total": 58,
  "replacement_api": "sklearn.compose._column_transformer.ColumnTransformer.get_feature_names_out",
  "threshold_10pct": 5.8,
  "vi_minus_1": {
    "mapBased": {
      "rank": 2,
      "score": 0.541961
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.575758
    },
    "treeBased": {
      "rank": 4,
      "score": 0.5
    }
  },
  "vi": {
    "mapBased": {
      "rank": 2,
      "score": 0.468606
    },
    "tokenBased": {
      "rank": 7,
      "score": 0.4
    },
    "treeBased": {
      "rank": 6,
      "score": 0.417431
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 2,
      "vi_rank": 2,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 7,
      "delta": -6,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 4,
      "vi_rank": 6,
      "delta": -2,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `sklearn.compose._column_transformer.ColumnTransformer.get_feature_names/Vi-1_0.22.2.py`
- **new**: `sklearn.compose._column_transformer.ColumnTransformer.get_feature_names/Vi_0.23.0.py`
- **+15 / -7**

```diff
--- sklearn.compose._column_transformer.ColumnTransformer.get_feature_names/Vi-1_0.22.2.py
+++ sklearn.compose._column_transformer.ColumnTransformer.get_feature_names/Vi_0.23.0.py
@@ -2,14 +2,22 @@
         
         check_is_fitted(self)
         feature_names = []
-        for name, trans, _, _ in self._iter(fitted=True):
-            if trans == 'drop':
+        for name, trans, column, _ in self._iter(fitted=True):
+            if trans == 'drop' or (
+                    hasattr(column, '__len__') and not len(column)):
                 continue
-            elif trans == 'passthrough':
-                raise NotImplementedError(
-                    "get_feature_names is not yet supported when using "
-                    "a 'passthrough' transformer.")
-            elif not hasattr(trans, 'get_feature_names'):
+            if trans == 'passthrough':
+                if hasattr(self, '_df_columns'):
+                    if ((not isinstance(column, slice))
+                            and all(isinstance(col, str) for col in column)):
+                        feature_names.extend(column)
+                    else:
+                        feature_names.extend(self._df_columns[column])
+                else:
+                    indices = np.arange(self._n_features)
+                    feature_names.extend(['x%d' % i for i in indices[column]])
+                continue
+            if not hasattr(trans, 'get_feature_names'):
                 raise AttributeError("Transformer %s (type %s) does not "
                                      "provide get_feature_names."
                                      % (str(name), type(trans).__name__))
```

```json
{
  "old_file": "sklearn.compose._column_transformer.ColumnTransformer.get_feature_names/Vi-1_0.22.2.py",
  "new_file": "sklearn.compose._column_transformer.ColumnTransformer.get_feature_names/Vi_0.23.0.py",
  "lines_added": 15,
  "lines_removed": 7
}
```
