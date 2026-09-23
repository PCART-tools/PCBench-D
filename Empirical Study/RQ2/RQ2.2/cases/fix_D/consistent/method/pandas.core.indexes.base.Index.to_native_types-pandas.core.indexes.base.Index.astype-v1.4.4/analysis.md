# 一、突变情况分析

- **Total**: 586
- **替代API**: `pandas.core.indexes.base.Index.astype`
- **10% 阈值**: 58.6

## Vi-1 (v1.1.5-v1.4.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 508 | 0.3046 |
| tokenBased | 500 | 0.1228 |
| treeBased | 531 | 0.2388 |

## Vi (v1.1.5-v1.5.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 560 | 0.2133 |
| tokenBased | 564 | 0.0921 |
| treeBased | 566 | 0.1815 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 508 | 560 | -52 | false |
| tokenBased | 500 | 564 | -64 | true |
| treeBased | 531 | 566 | -35 | false |

```json
{
  "total": 586,
  "replacement_api": "pandas.core.indexes.base.Index.astype",
  "threshold_10pct": 58.6,
  "vi_minus_1": {
    "mapBased": {
      "rank": 508,
      "score": 0.30462
    },
    "tokenBased": {
      "rank": 500,
      "score": 0.122807
    },
    "treeBased": {
      "rank": 531,
      "score": 0.238806
    }
  },
  "vi": {
    "mapBased": {
      "rank": 560,
      "score": 0.213309
    },
    "tokenBased": {
      "rank": 564,
      "score": 0.092105
    },
    "treeBased": {
      "rank": 566,
      "score": 0.181481
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 508,
      "vi_rank": 560,
      "delta": -52,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 500,
      "vi_rank": 564,
      "delta": -64,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 531,
      "vi_rank": 566,
      "delta": -35,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.4.4/pandas.core.indexes.base.Index.astype.py`
- **new**: `R_candidates/Vi_v1.5.0/pandas.core.indexes.base.Index.astype.py`
- **+31 / -10**

```diff
--- R_candidates/Vi-1_v1.4.4/pandas.core.indexes.base.Index.astype.py
+++ R_candidates/Vi_v1.5.0/pandas.core.indexes.base.Index.astype.py
@@ -7,20 +7,23 @@
 
             return self.copy() if copy else self
 
-        if (
-            self.dtype == np.dtype("M8[ns]")
-            and isinstance(dtype, np.dtype)
-            and dtype.kind == "M"
-            and dtype != np.dtype("M8[ns]")
-        ):
+        values = self._data
+        if isinstance(values, ExtensionArray):
+            if isinstance(dtype, np.dtype) and dtype.kind == "M" and is_unitless(dtype):
 
 
-            raise TypeError(f"Cannot cast {type(self).__name__} to dtype")
+                raise TypeError(f"Cannot cast {type(self).__name__} to dtype")
 
-        values = self._data
-        if isinstance(values, ExtensionArray):
             with rewrite_exception(type(values).__name__, type(self).__name__):
                 new_values = values.astype(dtype, copy=copy)
+
+        elif is_float_dtype(self.dtype) and needs_i8_conversion(dtype):
+
+
+            raise TypeError(
+                f"Cannot convert Float64Index to dtype {dtype}; integer "
+                "values are required for conversion"
+            )
 
         elif isinstance(dtype, ExtensionDtype):
             cls = dtype.construct_array_type()
@@ -30,11 +33,29 @@
 
         else:
             try:
-                new_values = values.astype(dtype, copy=copy)
+                if dtype == str:
+
+                    new_values = values.astype(dtype, copy=copy)
+                else:
+
+                    new_values = astype_nansafe(values, dtype=dtype, copy=copy)
+            except IntCastingNaNError:
+                raise
             except (TypeError, ValueError) as err:
+                if dtype.kind == "u" and "losslessly" in str(err):
+
+                    raise
                 raise TypeError(
                     f"Cannot cast {type(self).__name__} to dtype {dtype}"
                 ) from err
 
 
+        if self._is_backward_compat_public_numeric_index:
+
+
+
+            if isinstance(dtype, np.dtype) and is_numeric_dtype(dtype):
+                return self._constructor(
+                    new_values, name=self.name, dtype=dtype, copy=False
+                )
         return Index(new_values, name=self.name, dtype=new_values.dtype, copy=False)
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.4.4/pandas.core.indexes.base.Index.astype.py",
  "new_file": "R_candidates/Vi_v1.5.0/pandas.core.indexes.base.Index.astype.py",
  "lines_added": 31,
  "lines_removed": 10
}
```
