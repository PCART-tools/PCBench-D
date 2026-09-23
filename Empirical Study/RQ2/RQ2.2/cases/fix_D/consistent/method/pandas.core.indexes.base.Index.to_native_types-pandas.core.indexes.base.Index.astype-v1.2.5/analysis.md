# 一、突变情况分析

- **Total**: 624
- **替代API**: `pandas.core.indexes.base.Index.astype`
- **10% 阈值**: 62.4

## Vi-1 (v1.1.5-v1.2.5)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 506 | 0.3672 |
| tokenBased | 342 | 0.1963 |
| treeBased | 532 | 0.3103 |

## Vi (v1.1.5-v1.3.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 483 | 0.3543 |
| tokenBased | 290 | 0.2000 |
| treeBased | 467 | 0.3261 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 506 | 483 | +23 | false |
| tokenBased | 342 | 290 | +52 | false |
| treeBased | 532 | 467 | +65 | true |

```json
{
  "total": 624,
  "replacement_api": "pandas.core.indexes.base.Index.astype",
  "threshold_10pct": 62.4,
  "vi_minus_1": {
    "mapBased": {
      "rank": 506,
      "score": 0.367215
    },
    "tokenBased": {
      "rank": 342,
      "score": 0.196262
    },
    "treeBased": {
      "rank": 532,
      "score": 0.310345
    }
  },
  "vi": {
    "mapBased": {
      "rank": 483,
      "score": 0.354308
    },
    "tokenBased": {
      "rank": 290,
      "score": 0.2
    },
    "treeBased": {
      "rank": 467,
      "score": 0.326087
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 506,
      "vi_rank": 483,
      "delta": 23,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 342,
      "vi_rank": 290,
      "delta": 52,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 532,
      "vi_rank": 467,
      "delta": 65,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.2.5/pandas.core.indexes.base.Index.astype.py`
- **new**: `R_candidates/Vi_v1.3.0/pandas.core.indexes.base.Index.astype.py`
- **+4 / -9**

```diff
--- R_candidates/Vi-1_v1.2.5/pandas.core.indexes.base.Index.astype.py
+++ R_candidates/Vi_v1.3.0/pandas.core.indexes.base.Index.astype.py
@@ -6,15 +6,10 @@
         if is_dtype_equal(self.dtype, dtype):
             return self.copy() if copy else self
 
-        elif is_categorical_dtype(dtype):
-            from pandas.core.indexes.category import CategoricalIndex
-
-            return CategoricalIndex(
-                self._values, name=self.name, dtype=dtype, copy=copy
-            )
-
-        elif is_extension_array_dtype(dtype):
-            return Index(np.asarray(self), name=self.name, dtype=dtype, copy=copy)
+        elif isinstance(dtype, ExtensionDtype):
+            cls = dtype.construct_array_type()
+            new_values = cls._from_sequence(self, dtype=dtype, copy=False)
+            return Index(new_values, dtype=dtype, copy=copy, name=self.name)
 
         try:
             casted = self._values.astype(dtype, copy=copy)
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.2.5/pandas.core.indexes.base.Index.astype.py",
  "new_file": "R_candidates/Vi_v1.3.0/pandas.core.indexes.base.Index.astype.py",
  "lines_added": 4,
  "lines_removed": 9
}
```
