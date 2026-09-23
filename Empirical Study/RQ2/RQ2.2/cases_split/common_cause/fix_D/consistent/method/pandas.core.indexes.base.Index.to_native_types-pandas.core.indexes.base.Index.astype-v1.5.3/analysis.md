# 一、突变情况分析

- **Total**: 590
- **替代API**: `pandas.core.indexes.base.Index.astype`
- **10% 阈值**: 59.0

## Vi-1 (v1.1.5-v1.5.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 561 | 0.2133 |
| tokenBased | 565 | 0.0921 |
| treeBased | 567 | 0.1815 |

## Vi (v1.1.5-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 493 | 0.2946 |
| tokenBased | 400 | 0.1560 |
| treeBased | 494 | 0.2765 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 561 | 493 | +68 | true |
| tokenBased | 565 | 400 | +165 | true |
| treeBased | 567 | 494 | +73 | true |

```json
{
  "total": 590,
  "replacement_api": "pandas.core.indexes.base.Index.astype",
  "threshold_10pct": 59.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 561,
      "score": 0.213309
    },
    "tokenBased": {
      "rank": 565,
      "score": 0.092105
    },
    "treeBased": {
      "rank": 567,
      "score": 0.181481
    }
  },
  "vi": {
    "mapBased": {
      "rank": 493,
      "score": 0.294566
    },
    "tokenBased": {
      "rank": 400,
      "score": 0.156028
    },
    "treeBased": {
      "rank": 494,
      "score": 0.276471
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 561,
      "vi_rank": 493,
      "delta": 68,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 565,
      "vi_rank": 400,
      "delta": 165,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 567,
      "vi_rank": 494,
      "delta": 73,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.5.3/pandas.core.indexes.base.Index.astype.py`
- **new**: `R_candidates/Vi_v2.0.0/pandas.core.indexes.base.Index.astype.py`
- **+10 / -37**

```diff
--- R_candidates/Vi-1_v1.5.3/pandas.core.indexes.base.Index.astype.py
+++ R_candidates/Vi_v2.0.0/pandas.core.indexes.base.Index.astype.py
@@ -9,21 +9,8 @@
 
         values = self._data
         if isinstance(values, ExtensionArray):
-            if isinstance(dtype, np.dtype) and dtype.kind == "M" and is_unitless(dtype):
-
-
-                raise TypeError(f"Cannot cast {type(self).__name__} to dtype")
-
             with rewrite_exception(type(values).__name__, type(self).__name__):
                 new_values = values.astype(dtype, copy=copy)
-
-        elif is_float_dtype(self.dtype) and needs_i8_conversion(dtype):
-
-
-            raise TypeError(
-                f"Cannot convert Float64Index to dtype {dtype}; integer "
-                "values are required for conversion"
-            )
 
         elif isinstance(dtype, ExtensionDtype):
             cls = dtype.construct_array_type()
@@ -32,30 +19,16 @@
             new_values = cls._from_sequence(self, dtype=dtype, copy=copy)
 
         else:
-            try:
-                if dtype == str:
 
-                    new_values = values.astype(dtype, copy=copy)
-                else:
-
-                    new_values = astype_nansafe(values, dtype=dtype, copy=copy)
-            except IntCastingNaNError:
-                raise
-            except (TypeError, ValueError) as err:
-                if dtype.kind == "u" and "losslessly" in str(err):
-
-                    raise
-                raise TypeError(
-                    f"Cannot cast {type(self).__name__} to dtype {dtype}"
-                ) from err
+            new_values = astype_array(values, dtype=dtype, copy=copy)
 
 
-        if self._is_backward_compat_public_numeric_index:
-
-
-
-            if isinstance(dtype, np.dtype) and is_numeric_dtype(dtype):
-                return self._constructor(
-                    new_values, name=self.name, dtype=dtype, copy=False
-                )
-        return Index(new_values, name=self.name, dtype=new_values.dtype, copy=False)
+        result = Index(new_values, name=self.name, dtype=new_values.dtype, copy=False)
+        if (
+            not copy
+            and self._references is not None
+            and astype_is_view(self.dtype, dtype)
+        ):
+            result._references = self._references
+            result._references.add_index_reference(result)
+        return result
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.5.3/pandas.core.indexes.base.Index.astype.py",
  "new_file": "R_candidates/Vi_v2.0.0/pandas.core.indexes.base.Index.astype.py",
  "lines_added": 10,
  "lines_removed": 37
}
```
