# 一、突变情况分析

- **Total**: 21
- **替代API**: `pandas.core.indexes.base.Index`
- **10% 阈值**: 2.1

## Vi-1 (v1.2.5-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 20 | 0.0277 |
| tokenBased | 20 | 0.0210 |

## Vi (v1.3.0-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 8 | 0.0096 |
| tokenBased | 21 | 0.0029 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 20 | 8 | +12 | true |
| tokenBased | 20 | 21 | -1 | false |

```json
{
  "total": 21,
  "replacement_api": "pandas.core.indexes.base.Index",
  "threshold_10pct": 2.1,
  "vi_minus_1": {
    "mapBased": {
      "rank": 20,
      "score": 0.027652
    },
    "tokenBased": {
      "rank": 20,
      "score": 0.020961
    }
  },
  "vi": {
    "mapBased": {
      "rank": 8,
      "score": 0.009615
    },
    "tokenBased": {
      "rank": 21,
      "score": 0.002869
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 20,
      "vi_rank": 8,
      "delta": 12,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 20,
      "vi_rank": 21,
      "delta": -1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `pandas.core.indexes.numeric.Float64Index/Vi-1_v1.2.5.py`
- **new**: `pandas.core.indexes.numeric.Float64Index/Vi_v1.3.0.py`
- **+8 / -80**

```diff
--- pandas.core.indexes.numeric.Float64Index/Vi-1_v1.2.5.py
+++ pandas.core.indexes.numeric.Float64Index/Vi_v1.3.0.py
@@ -1,85 +1,13 @@
 class Float64Index(NumericIndex):
-    __doc__ = _num_index_shared_docs["class_descr"] % _float64_descr_args
+    _index_descr_args = {
+        "klass": "Float64Index",
+        "dtype": "float64",
+        "ltype": "float",
+        "extra": "",
+    }
+    __doc__ = _num_index_shared_docs["class_descr"] % _index_descr_args
 
     _typ = "float64index"
     _engine_type = libindex.Float64Engine
     _default_dtype = np.dtype(np.float64)
-
-    @property
-    def inferred_type(self) -> str:
-        
-        return "floating"
-
-    @doc(Index.astype)
-    def astype(self, dtype, copy=True):
-        dtype = pandas_dtype(dtype)
-        if needs_i8_conversion(dtype):
-            raise TypeError(
-                f"Cannot convert Float64Index to dtype {dtype}; integer "
-                "values are required for conversion"
-            )
-        elif is_integer_dtype(dtype) and not is_extension_array_dtype(dtype):
-
-
-            arr = astype_nansafe(self._values, dtype=dtype)
-            return Int64Index(arr, name=self.name)
-        return super().astype(dtype, copy=copy)
-
-
-
-
-    @doc(Index._should_fallback_to_positional)
-    def _should_fallback_to_positional(self) -> bool:
-        return False
-
-    @doc(Index._convert_slice_indexer)
-    def _convert_slice_indexer(self, key: slice, kind: str):
-        assert kind in ["loc", "getitem"]
-
-
-
-        return self.slice_indexer(key.start, key.stop, key.step, kind=kind)
-
-    @doc(Index.get_loc)
-    def get_loc(self, key, method=None, tolerance=None):
-        if is_bool(key):
-
-            raise KeyError(key)
-
-        if is_float(key) and np.isnan(key):
-            nan_idxs = self._nan_idxs
-            if not len(nan_idxs):
-                raise KeyError(key)
-            elif len(nan_idxs) == 1:
-                return nan_idxs[0]
-            return nan_idxs
-
-        return super().get_loc(key, method=method, tolerance=tolerance)
-
-
-
-    def _format_native_types(
-        self, na_rep="", float_format=None, decimal=".", quoting=None, **kwargs
-    ):
-        from pandas.io.formats.format import FloatArrayFormatter
-
-        formatter = FloatArrayFormatter(
-            self._values,
-            na_rep=na_rep,
-            float_format=float_format,
-            decimal=decimal,
-            quoting=quoting,
-            fixed_width=False,
-        )
-        return formatter.get_result_as_array()
-
-    def __contains__(self, other: Any) -> bool:
-        hash(other)
-        if super().__contains__(other):
-            return True
-
-        return is_float(other) and np.isnan(other) and self.hasnans
-
-    def _can_union_without_object_cast(self, other) -> bool:
-
-        return is_numeric_dtype(other.dtype)
+    _dtype_validation_metadata = (is_float_dtype, "float")
```

```json
{
  "old_file": "pandas.core.indexes.numeric.Float64Index/Vi-1_v1.2.5.py",
  "new_file": "pandas.core.indexes.numeric.Float64Index/Vi_v1.3.0.py",
  "lines_added": 8,
  "lines_removed": 80
}
```
