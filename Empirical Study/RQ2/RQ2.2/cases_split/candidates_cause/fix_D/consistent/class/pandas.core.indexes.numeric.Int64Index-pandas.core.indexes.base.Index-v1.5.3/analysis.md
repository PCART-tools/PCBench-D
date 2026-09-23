# 一、突变情况分析

- **Total**: 25
- **替代API**: `pandas.core.indexes.base.Index`
- **10% 阈值**: 2.5

## Vi-1 (v1.3.5-v1.5.3)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 12 | 0.0089 |
| tokenBased | 25 | 0.0028 |

## Vi (v1.3.5-v2.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 8 | 0.0096 |
| tokenBased | 21 | 0.0029 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 12 | 8 | +4 | true |
| tokenBased | 25 | 21 | +4 | true |

```json
{
  "total": 25,
  "replacement_api": "pandas.core.indexes.base.Index",
  "threshold_10pct": 2.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 12,
      "score": 0.008929
    },
    "tokenBased": {
      "rank": 25,
      "score": 0.002773
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
      "vi1_rank": 12,
      "vi_rank": 8,
      "delta": 4,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 25,
      "vi_rank": 21,
      "delta": 4,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_v1.5.3/pandas.core.indexes.base.Index.py`
- **new**: `R_candidates/Vi_v2.0.0/pandas.core.indexes.base.Index.py`
- **+695 / -854**

```diff
--- R_candidates/Vi-1_v1.5.3/pandas.core.indexes.base.Index.py
+++ R_candidates/Vi_v2.0.0/pandas.core.indexes.base.Index.py
@@ -2,13 +2,6 @@
     
 
 
-    _hidden_attrs: frozenset[str] = (
-        PandasObject._hidden_attrs
-        | IndexOpsMixin._hidden_attrs
-        | frozenset(["contains", "set_value"])
-    )
-
-
     _join_precedence = 1
 
 
@@ -19,11 +12,12 @@
     @final
     def _left_indexer_unique(self: _IndexT, other: _IndexT) -> npt.NDArray[np.intp]:
 
-        sv = self._get_engine_target()
-        ov = other._get_engine_target()
+        sv = self._get_join_target()
+        ov = other._get_join_target()
 
         sv = cast(np.ndarray, sv)
         ov = cast(np.ndarray, ov)
+
         return libjoin.left_join_indexer_unique(sv, ov)
 
     @final
@@ -31,8 +25,8 @@
         self: _IndexT, other: _IndexT
     ) -> tuple[ArrayLike, npt.NDArray[np.intp], npt.NDArray[np.intp]]:
 
-        sv = self._get_engine_target()
-        ov = other._get_engine_target()
+        sv = self._get_join_target()
+        ov = other._get_join_target()
 
         sv = cast(np.ndarray, sv)
         ov = cast(np.ndarray, ov)
@@ -45,8 +39,8 @@
         self: _IndexT, other: _IndexT
     ) -> tuple[ArrayLike, npt.NDArray[np.intp], npt.NDArray[np.intp]]:
 
-        sv = self._get_engine_target()
-        ov = other._get_engine_target()
+        sv = self._get_join_target()
+        ov = other._get_join_target()
 
         sv = cast(np.ndarray, sv)
         ov = cast(np.ndarray, ov)
@@ -59,8 +53,8 @@
         self: _IndexT, other: _IndexT
     ) -> tuple[ArrayLike, npt.NDArray[np.intp], npt.NDArray[np.intp]]:
 
-        sv = self._get_engine_target()
-        ov = other._get_engine_target()
+        sv = self._get_join_target()
+        ov = other._get_join_target()
 
         sv = cast(np.ndarray, sv)
         ov = cast(np.ndarray, ov)
@@ -82,19 +76,31 @@
     _no_setting_name: bool = False
     _comparables: list[str] = ["name"]
     _attributes: list[str] = ["name"]
-    _is_numeric_dtype: bool = False
-    _can_hold_strings: bool = True
-
-
-
-
-    _is_backward_compat_public_numeric_index: bool = False
+
+    @cache_readonly
+    def _can_hold_strings(self) -> bool:
+        return not is_numeric_dtype(self)
+
+    _engine_types: dict[np.dtype | ExtensionDtype, type[libindex.IndexEngine]] = {
+        np.dtype(np.int8): libindex.Int8Engine,
+        np.dtype(np.int16): libindex.Int16Engine,
+        np.dtype(np.int32): libindex.Int32Engine,
+        np.dtype(np.int64): libindex.Int64Engine,
+        np.dtype(np.uint8): libindex.UInt8Engine,
+        np.dtype(np.uint16): libindex.UInt16Engine,
+        np.dtype(np.uint32): libindex.UInt32Engine,
+        np.dtype(np.uint64): libindex.UInt64Engine,
+        np.dtype(np.float32): libindex.Float32Engine,
+        np.dtype(np.float64): libindex.Float64Engine,
+        np.dtype(np.complex64): libindex.Complex64Engine,
+        np.dtype(np.complex128): libindex.Complex128Engine,
+    }
 
     @property
     def _engine_type(
         self,
     ) -> type[libindex.IndexEngine] | type[libindex.ExtensionEngine]:
-        return libindex.ObjectEngine
+        return self._engine_types.get(self.dtype, libindex.ObjectEngine)
 
 
 
@@ -104,42 +110,31 @@
 
     str = CachedAccessor("str", StringMethods)
 
+    _references = None
+
 
 
 
     def __new__(
-        cls, data=None, dtype=None, copy=False, name=None, tupleize_cols=True, **kwargs
+        cls,
+        data=None,
+        dtype=None,
+        copy: bool = False,
+        name=None,
+        tupleize_cols: bool = True,
     ) -> Index:
-
-        if kwargs:
-            warnings.warn(
-                "Passing keywords other than 'data', 'dtype', 'copy', 'name', "
-                "'tupleize_cols' is deprecated and will raise TypeError in a "
-                "future version.  Use the specific Index subclass directly instead.",
-                FutureWarning,
-                stacklevel=find_stack_level(),
-            )
-
-        from pandas.core.arrays import PandasArray
         from pandas.core.indexes.range import RangeIndex
 
         name = maybe_extract_name(name, data, cls)
 
         if dtype is not None:
             dtype = pandas_dtype(dtype)
-        if "tz" in kwargs:
-            tz = kwargs.pop("tz")
-            validate_tz_from_dtype(dtype, tz)
-            dtype = tz_to_dtype(tz)
-
-        if type(data) is PandasArray:
-
-
-            data = data.to_numpy()
-        if isinstance(dtype, PandasDtype):
-            dtype = dtype.numpy_dtype
 
         data_dtype = getattr(data, "dtype", None)
+
+        refs = None
+        if not copy and isinstance(data, (ABCSeries, Index)):
+            refs = data._references
 
 
         if isinstance(data, (range, RangeIndex)):
@@ -150,84 +145,33 @@
 
         elif is_ea_or_datetimelike_dtype(dtype):
 
-            klass = cls._dtype_to_subclass(dtype)
-            if klass is not Index:
-                return klass(data, dtype=dtype, copy=copy, name=name, **kwargs)
-
-            ea_cls = dtype.construct_array_type()
-            data = ea_cls._from_sequence(data, dtype=dtype, copy=copy)
-            disallow_kwargs(kwargs)
-            return Index._simple_new(data, name=name)
+            pass
 
         elif is_ea_or_datetimelike_dtype(data_dtype):
-            data_dtype = cast(DtypeObj, data_dtype)
-            klass = cls._dtype_to_subclass(data_dtype)
-            if klass is not Index:
-                result = klass(data, copy=copy, name=name, **kwargs)
-                if dtype is not None:
-                    return result.astype(dtype, copy=False)
-                return result
-            elif dtype is not None:
-
-                data = data.astype(dtype, copy=False)
-
-            disallow_kwargs(kwargs)
-            data = extract_array(data, extract_numpy=True)
-            return Index._simple_new(data, name=name)
-
-
-        elif (
-            isinstance(data, Index)
-            and data._is_backward_compat_public_numeric_index
-            and dtype is None
-        ):
-            return data._constructor(data, name=name, copy=copy)
+            pass
+
         elif isinstance(data, (np.ndarray, Index, ABCSeries)):
-
             if isinstance(data, ABCMultiIndex):
                 data = data._values
 
-            if dtype is not None:
-
-
-
-
-
-                data = sanitize_array(data, None, dtype=dtype, copy=copy)
-
-                dtype = data.dtype
-
-            if data.dtype.kind in ["i", "u", "f"]:
-
-                arr = data
-            elif data.dtype.kind in ["b", "c"]:
-
-
-                arr = np.asarray(data)
-            else:
-                arr = com.asarray_tuplesafe(data, dtype=_dtype_obj)
-
-                if dtype is None:
-                    arr = _maybe_cast_data_without_dtype(
-                        arr, cast_numeric_deprecated=True
-                    )
-                    dtype = arr.dtype
-
-                    if kwargs:
-                        return cls(arr, dtype, copy=copy, name=name, **kwargs)
-
-            klass = cls._dtype_to_subclass(arr.dtype)
-            arr = klass._ensure_array(arr, dtype, copy)
-            disallow_kwargs(kwargs)
-            return klass._simple_new(arr, name)
+            if data.dtype.kind not in ["i", "u", "f", "b", "c", "m", "M"]:
+
+
+
+
+                data = com.asarray_tuplesafe(data, dtype=_dtype_obj)
 
         elif is_scalar(data):
-            raise cls._scalar_data_error(data)
+            raise cls._raise_scalar_data_error(data)
         elif hasattr(data, "__array__"):
-            return Index(np.asarray(data), dtype=dtype, copy=copy, name=name, **kwargs)
-        else:
-
-            if tupleize_cols and is_list_like(data):
+            return Index(np.asarray(data), dtype=dtype, copy=copy, name=name)
+        elif not is_list_like(data) and not isinstance(data, memoryview):
+
+
+            raise cls._raise_scalar_data_error(data)
+
+        else:
+            if tupleize_cols:
 
                 if is_iterator(data):
                     data = list(data)
@@ -237,19 +181,35 @@
 
                     from pandas.core.indexes.multi import MultiIndex
 
-                    return MultiIndex.from_tuples(
-                        data, names=name or kwargs.get("names")
-                    )
-
-
-            subarr = com.asarray_tuplesafe(data, dtype=_dtype_obj)
-            if dtype is None:
-
-                subarr = _maybe_cast_data_without_dtype(
-                    subarr, cast_numeric_deprecated=False
-                )
-                dtype = subarr.dtype
-            return Index(subarr, dtype=dtype, copy=copy, name=name, **kwargs)
+                    return MultiIndex.from_tuples(data, names=name)
+
+
+            if not isinstance(data, (list, tuple)):
+
+
+                data = list(data)
+            if len(data) == 0:
+
+                data = np.array(data, dtype=object)
+
+            if len(data) and isinstance(data[0], tuple):
+
+                data = com.asarray_tuplesafe(data, dtype=_dtype_obj)
+
+        try:
+            arr = sanitize_array(data, None, dtype=dtype, copy=copy)
+        except ValueError as err:
+            if "index must be specified when data is not list-like" in str(err):
+                raise cls._raise_scalar_data_error(data) from err
+            if "Data must be 1-dimensional" in str(err):
+                raise ValueError("Index data must be 1-dimensional") from err
+            raise
+        arr = ensure_wrapped_if_datetimelike(arr)
+
+        klass = cls._dtype_to_subclass(arr.dtype)
+
+        arr = klass._ensure_array(arr, arr.dtype, copy=False)
+        return klass._simple_new(arr, name, refs=refs)
 
     @classmethod
     def _ensure_array(cls, data, dtype, copy: bool):
@@ -257,6 +217,10 @@
         if data.ndim > 1:
 
             raise ValueError("Index data must be 1-dimensional")
+        elif dtype == np.float16:
+
+            raise NotImplementedError("float16 indexes are not supported")
+
         if copy:
 
 
@@ -286,17 +250,6 @@
 
                 return PeriodIndex
 
-            elif isinstance(dtype, SparseDtype):
-                warnings.warn(
-                    "In a future version, passing a SparseArray to pd.Index "
-                    "will store that array directly instead of converting to a "
-                    "dense numpy ndarray. To retain the old behavior, use "
-                    "pd.Index(arr.to_numpy()) instead",
-                    FutureWarning,
-                    stacklevel=find_stack_level(),
-                )
-                return cls._dtype_to_subclass(dtype.subtype)
-
             return Index
 
         if dtype.kind == "M":
@@ -309,57 +262,32 @@
 
             return TimedeltaIndex
 
-        elif is_float_dtype(dtype):
-            from pandas.core.api import Float64Index
-
-            return Float64Index
-        elif is_unsigned_integer_dtype(dtype):
-            from pandas.core.api import UInt64Index
-
-            return UInt64Index
-        elif is_signed_integer_dtype(dtype):
-            from pandas.core.api import Int64Index
-
-            return Int64Index
-
-        elif dtype == _dtype_obj:
+        elif dtype.kind == "O":
 
             return Index
 
-        elif issubclass(
-            dtype.type, (str, bool, np.bool_, complex, np.complex64, np.complex128)
-        ):
+        elif issubclass(dtype.type, str) or is_numeric_dtype(dtype):
             return Index
 
         raise NotImplementedError(dtype)
 
-    """
-    NOTE for new Index creation:
-
-    - _simple_new: It returns new Index with the same type as the caller.
-      All metadata (such as name) must be provided by caller's responsibility.
-      Using _shallow_copy is recommended because it fills these metadata
-      otherwise specified.
-
-    - _shallow_copy: It returns new Index with the same type (using
-      _simple_new), but fills caller's metadata otherwise specified. Passed
-      kwargs will overwrite corresponding metadata.
-
-    See each method's docstring.
-    """
-
-    @property
-    def asi8(self):
-        
-        warnings.warn(
-            "Index.asi8 is deprecated and will be removed in a future version.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-        return None
+
+
+
+
+
+
+
+
+
+
+
+
 
     @classmethod
-    def _simple_new(cls: type[_IndexT], values, name: Hashable = None) -> _IndexT:
+    def _simple_new(
+        cls: type[_IndexT], values: ArrayLike, name: Hashable = None, refs=None
+    ) -> _IndexT:
         
         assert isinstance(values, cls._data_cls), type(values)
 
@@ -368,15 +296,18 @@
         result._name = name
         result._cache = {}
         result._reset_identity()
+        if refs is not None:
+            result._references = refs
+        else:
+            result._references = BlockValuesRefs()
+        result._references.add_index_reference(result)
 
         return result
 
     @classmethod
     def _with_infer(cls, *args, **kwargs):
         
-        with warnings.catch_warnings():
-            warnings.filterwarnings("ignore", ".*the Index constructor", FutureWarning)
-            result = cls(*args, **kwargs)
+        result = cls(*args, **kwargs)
 
         if result.dtype == _dtype_obj and not result._is_multi:
 
@@ -423,26 +354,15 @@
 
 
 
-    @final
-    def _get_attributes_dict(self) -> dict[str_t, Any]:
-        
-        warnings.warn(
-            "The Index._get_attributes_dict method is deprecated, and will be "
-            "removed in a future version",
-            DeprecationWarning,
-            stacklevel=find_stack_level(),
-        )
-        return {k: getattr(self, k, None) for k in self._attributes}
-
     def _shallow_copy(self: _IndexT, values, name: Hashable = no_default) -> _IndexT:
         
         name = self._name if name is no_default else name
 
-        return self._simple_new(values, name=name)
+        return self._simple_new(values, name=name, refs=self._references)
 
     def _view(self: _IndexT) -> _IndexT:
         
-        result = self._simple_new(self._values, name=self._name)
+        result = self._simple_new(self._values, name=self._name, refs=self._references)
 
         result._cache = self._cache
         return result
@@ -478,14 +398,18 @@
     @cache_readonly
     def _engine(
         self,
-    ) -> libindex.IndexEngine | libindex.ExtensionEngine:
+    ) -> libindex.IndexEngine | libindex.ExtensionEngine | libindex.MaskedIndexEngine:
 
         target_values = self._get_engine_target()
-        if (
-            isinstance(target_values, ExtensionArray)
-            and self._engine_type is libindex.ObjectEngine
-        ):
-            return libindex.ExtensionEngine(target_values)
+        if isinstance(target_values, ExtensionArray):
+            if isinstance(target_values, (BaseMaskedArray, ArrowExtensionArray)):
+                try:
+                    return _masked_engines[target_values.dtype.name](target_values)
+                except KeyError:
+
+                    pass
+            elif self._engine_type is libindex.ObjectEngine:
+                return libindex.ExtensionEngine(target_values)
 
         target_values = cast(np.ndarray, target_values)
 
@@ -496,6 +420,13 @@
             return libindex.Complex64Engine(target_values)
         elif target_values.dtype == np.complex128:
             return libindex.Complex128Engine(target_values)
+        elif needs_i8_conversion(self.dtype):
+
+
+
+
+
+            target_values = self._data._ndarray
 
 
 
@@ -527,19 +458,11 @@
         if any(isinstance(other, (ABCSeries, ABCDataFrame)) for other in inputs):
             return NotImplemented
 
-
-
-
-
-        if not (
-            method == "__call__"
-            and ufunc in (np.bitwise_and, np.bitwise_or, np.bitwise_xor)
-        ):
-            result = arraylike.maybe_dispatch_ufunc_to_dunder_op(
-                self, ufunc, method, *inputs, **kwargs
-            )
-            if result is not NotImplemented:
-                return result
+        result = arraylike.maybe_dispatch_ufunc_to_dunder_op(
+            self, ufunc, method, *inputs, **kwargs
+        )
+        if result is not NotImplemented:
+            return result
 
         if "out" in kwargs:
 
@@ -560,6 +483,9 @@
 
             return tuple(self.__array_wrap__(x) for x in result)
 
+        if result.dtype == np.float16:
+            result = result.astype(np.float32)
+
         return self.__array_wrap__(result)
 
     def __array_wrap__(self, result, context=None):
@@ -576,26 +502,11 @@
         return self._data.dtype
 
     @final
-    def ravel(self, order="C"):
-        
-        warnings.warn(
-            "Index.ravel returning ndarray is deprecated; in a future version "
-            "this will return a view on self.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-        if needs_i8_conversion(self.dtype):
-
-
-            values = self._data._ndarray
-        elif is_interval_dtype(self.dtype):
-            values = np.asarray(self._data)
-        else:
-            values = self._get_engine_target()
-        return values.ravel(order=order)
+    def ravel(self, order: str_t = "C") -> Index:
+        
+        return self[:]
 
     def view(self, cls=None):
-
 
 
         if cls is not None and not hasattr(cls, "_typ"):
@@ -616,7 +527,7 @@
 
                 arr_cls = idx_cls._data_cls
                 arr = arr_cls(self._data.view("i8"), dtype=dtype)
-                return idx_cls._simple_new(arr, name=self.name)
+                return idx_cls._simple_new(arr, name=self.name, refs=self._references)
 
             result = self._data.view(cls)
         else:
@@ -636,22 +547,9 @@
 
         values = self._data
         if isinstance(values, ExtensionArray):
-            if isinstance(dtype, np.dtype) and dtype.kind == "M" and is_unitless(dtype):
-
-
-                raise TypeError(f"Cannot cast {type(self).__name__} to dtype")
-
             with rewrite_exception(type(values).__name__, type(self).__name__):
                 new_values = values.astype(dtype, copy=copy)
 
-        elif is_float_dtype(self.dtype) and needs_i8_conversion(dtype):
-
-
-            raise TypeError(
-                f"Cannot convert Float64Index to dtype {dtype}; integer "
-                "values are required for conversion"
-            )
-
         elif isinstance(dtype, ExtensionDtype):
             cls = dtype.construct_array_type()
 
@@ -659,33 +557,19 @@
             new_values = cls._from_sequence(self, dtype=dtype, copy=copy)
 
         else:
-            try:
-                if dtype == str:
-
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
-
-
-        if self._is_backward_compat_public_numeric_index:
-
-
-
-            if isinstance(dtype, np.dtype) and is_numeric_dtype(dtype):
-                return self._constructor(
-                    new_values, name=self.name, dtype=dtype, copy=False
-                )
-        return Index(new_values, name=self.name, dtype=new_values.dtype, copy=False)
+
+            new_values = astype_array(values, dtype=dtype, copy=copy)
+
+
+        result = Index(new_values, name=self.name, dtype=new_values.dtype, copy=False)
+        if (
+            not copy
+            and self._references is not None
+            and astype_is_view(self.dtype, dtype)
+        ):
+            result._references = self._references
+            result._references.add_index_reference(result)
+        return result
 
     _index_shared_docs[
         "take"
@@ -719,7 +603,12 @@
 
     @Appender(_index_shared_docs["take"] % _index_doc_kwargs)
     def take(
-        self, indices, axis: int = 0, allow_fill: bool = True, fill_value=None, **kwargs
+        self,
+        indices,
+        axis: Axis = 0,
+        allow_fill: bool = True,
+        fill_value=None,
+        **kwargs,
     ):
         if kwargs:
             nv.validate_take((), kwargs)
@@ -783,7 +672,7 @@
 
         Returns
         -------
-        repeated_index : %(klass)s
+        %(klass)s
             Newly created %(klass)s with repeated elements.
 
         See Also
@@ -818,33 +707,15 @@
         self: _IndexT,
         name: Hashable | None = None,
         deep: bool = False,
-        dtype: Dtype | None = None,
-        names: Sequence[Hashable] | None = None,
     ) -> _IndexT:
         
-        if names is not None:
-            warnings.warn(
-                "parameter names is deprecated and will be removed in a future "
-                "version. Use the name parameter instead.",
-                FutureWarning,
-                stacklevel=find_stack_level(),
-            )
-
-        name = self._validate_names(name=name, names=names, deep=deep)[0]
+
+        name = self._validate_names(name=name, deep=deep)[0]
         if deep:
             new_data = self._data.copy()
             new_index = type(self)._simple_new(new_data, name=name)
         else:
             new_index = self._rename(name=name)
-
-        if dtype:
-            warnings.warn(
-                "parameter dtype is deprecated and will be removed in a future "
-                "version. Use the astype method instead.",
-                FutureWarning,
-                stacklevel=find_stack_level(),
-            )
-            new_index = new_index.astype(dtype)
         return new_index
 
     @final
@@ -876,7 +747,6 @@
         return f"{klass_name}({data}{prepr})"
 
     def _format_space(self) -> str_t:
-
 
 
 
@@ -985,26 +855,31 @@
             result = trim_front(format_array(values, None, justify="left"))
         return header + result
 
-    @final
-    def to_native_types(self, slicer=None, **kwargs) -> np.ndarray:
-        
-        warnings.warn(
-            "The 'to_native_types' method is deprecated and will be removed in "
-            "a future version. Use 'astype(str)' instead.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-        values = self
-        if slicer is not None:
-            values = values[slicer]
-        return values._format_native_types(**kwargs)
-
     def _format_native_types(
-        self, *, na_rep="", quoting=None, **kwargs
+        self,
+        *,
+        na_rep: str_t = "",
+        decimal: str_t = ".",
+        float_format=None,
+        date_format=None,
+        quoting=None,
     ) -> npt.NDArray[np.object_]:
         
+        from pandas.io.formats.format import FloatArrayFormatter
+
+        if is_float_dtype(self.dtype) and not is_extension_array_dtype(self.dtype):
+            formatter = FloatArrayFormatter(
+                self._values,
+                na_rep=na_rep,
+                float_format=float_format,
+                decimal=decimal,
+                quoting=quoting,
+                fixed_width=False,
+            )
+            return formatter.get_result_as_array()
+
         mask = isna(self)
-        if not self.is_object() and not quoting:
+        if not is_object_dtype(self) and not quoting:
             values = np.asarray(self).astype(str)
         else:
             values = np.array(self, dtype=object, copy=True)
@@ -1043,6 +918,7 @@
         
         return self
 
+    @final
     def to_series(self, index=None, name: Hashable = None) -> Series:
         
         from pandas import Series
@@ -1059,17 +935,6 @@
     ) -> DataFrame:
         
         from pandas import DataFrame
-
-        if name is None:
-            warnings.warn(
-                "Explicitly passing `name=None` currently preserves the Index's name "
-                "or uses a default name of 0. This behaviour is deprecated, and in "
-                "the future `None` will be used as the name of the resulting "
-                "DataFrame column.",
-                FutureWarning,
-                stacklevel=find_stack_level(),
-            )
-            name = lib.no_default
 
         if name is lib.no_default:
             name = self._get_level_names()
@@ -1107,7 +972,7 @@
 
         if names is not None and name is not None:
             raise TypeError("Can only provide one of `names` and `name`")
-        elif names is None and name is None:
+        if names is None and name is None:
             new_names = deepcopy(self.names) if deep else self.names
         elif names is not None:
             if not is_list_like(names):
@@ -1135,7 +1000,7 @@
         from pandas.core.indexes.multi import MultiIndex
 
         if names is not None:
-            if isinstance(names, str) or isinstance(names, int):
+            if isinstance(names, (int, str)):
                 names = [names]
 
         if not isinstance(names, list) and names is not None:
@@ -1167,22 +1032,39 @@
 
     names = property(fset=_set_names, fget=_get_names)
 
-    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "names"])
-    def set_names(self, names, level=None, inplace: bool = False):
+    @overload
+    def set_names(
+        self: _IndexT, names, *, level=..., inplace: Literal[False] = ...
+    ) -> _IndexT:
+        ...
+
+    @overload
+    def set_names(self, names, *, level=..., inplace: Literal[True]) -> None:
+        ...
+
+    @overload
+    def set_names(
+        self: _IndexT, names, *, level=..., inplace: bool = ...
+    ) -> _IndexT | None:
+        ...
+
+    def set_names(
+        self: _IndexT, names, *, level=None, inplace: bool = False
+    ) -> _IndexT | None:
         
         if level is not None and not isinstance(self, ABCMultiIndex):
             raise ValueError("Level must be None for non-MultiIndex")
 
-        elif level is not None and not is_list_like(level) and is_list_like(names):
+        if level is not None and not is_list_like(level) and is_list_like(names):
             raise TypeError("Names must be a string when a single level is provided.")
 
-        elif not is_list_like(names) and level is None and self.nlevels > 1:
+        if not is_list_like(names) and level is None and self.nlevels > 1:
             raise TypeError("Must pass list-like as `names`.")
 
-        elif is_dict_like(names) and not isinstance(self, ABCMultiIndex):
+        if is_dict_like(names) and not isinstance(self, ABCMultiIndex):
             raise TypeError("Can only pass dict-like as `names` for MultiIndex.")
 
-        elif is_dict_like(names) and level is not None:
+        if is_dict_like(names) and level is not None:
             raise TypeError("Can not pass level for dictlike `names`.")
 
         if isinstance(self, ABCMultiIndex) and is_dict_like(names) and level is None:
@@ -1207,8 +1089,9 @@
         idx._set_names(names, level=level)
         if not inplace:
             return idx
-
-    def rename(self, name, inplace=False):
+        return None
+
+    def rename(self, name, inplace: bool = False):
         
         return self.set_names([name], inplace=inplace)
 
@@ -1233,7 +1116,7 @@
                     "Too many levels: Index has only 1 level, "
                     f"{level} is not a valid level number"
                 )
-            elif level > 0:
+            if level > 0:
                 raise IndexError(
                     f"Too many levels: Index has only 1 level, not {level + 1}"
                 )
@@ -1246,7 +1129,9 @@
         self._validate_index_level(level)
         return 0
 
-    def sortlevel(self, level=None, ascending=True, sort_remaining=None):
+    def sortlevel(
+        self, level=None, ascending: bool | list[bool] = True, sort_remaining=None
+    ):
         
         if not isinstance(ascending, (list, bool)):
             raise TypeError(
@@ -1272,7 +1157,7 @@
     get_level_values = _get_level_values
 
     @final
-    def droplevel(self, level=0):
+    def droplevel(self, level: IndexLabel = 0):
         
         if not isinstance(level, (tuple, list)):
             level = [level]
@@ -1337,22 +1222,6 @@
                 verify_integrity=False,
             )
 
-    def _get_grouper_for_level(
-        self,
-        mapper,
-        *,
-        level=None,
-        dropna: bool = True,
-    ) -> tuple[Index, npt.NDArray[np.signedinteger] | None, Index | None]:
-        
-        assert level is None or level == 0
-        if mapper is None:
-            grouper = self
-        else:
-            grouper = self.map(mapper)
-
-        return grouper, None, None
-
 
 
 
@@ -1370,101 +1239,132 @@
             return False
         return True
 
-    @final
     @property
-    def is_monotonic(self) -> bool:
+    def is_monotonic_increasing(self) -> bool:
+        
+        return self._engine.is_monotonic_increasing
+
+    @property
+    def is_monotonic_decreasing(self) -> bool:
+        
+        return self._engine.is_monotonic_decreasing
+
+    @final
+    @property
+    def _is_strictly_monotonic_increasing(self) -> bool:
+        
+        return self.is_unique and self.is_monotonic_increasing
+
+    @final
+    @property
+    def _is_strictly_monotonic_decreasing(self) -> bool:
+        
+        return self.is_unique and self.is_monotonic_decreasing
+
+    @cache_readonly
+    def is_unique(self) -> bool:
+        
+        return self._engine.is_unique
+
+    @final
+    @property
+    def has_duplicates(self) -> bool:
+        
+        return not self.is_unique
+
+    @final
+    def is_boolean(self) -> bool:
         
         warnings.warn(
-            "is_monotonic is deprecated and will be removed in a future version. "
-            "Use is_monotonic_increasing instead.",
+            f"{type(self).__name__}.is_boolean is deprecated. "
+            "Use pandas.api.types.is_bool_type instead.",
             FutureWarning,
             stacklevel=find_stack_level(),
         )
-        return self.is_monotonic_increasing
-
-    @property
-    def is_monotonic_increasing(self) -> bool:
-        
-        return self._engine.is_monotonic_increasing
-
-    @property
-    def is_monotonic_decreasing(self) -> bool:
-        
-        return self._engine.is_monotonic_decreasing
-
-    @final
-    @property
-    def _is_strictly_monotonic_increasing(self) -> bool:
-        
-        return self.is_unique and self.is_monotonic_increasing
-
-    @final
-    @property
-    def _is_strictly_monotonic_decreasing(self) -> bool:
-        
-        return self.is_unique and self.is_monotonic_decreasing
-
-    @cache_readonly
-    def is_unique(self) -> bool:
-        
-        return self._engine.is_unique
-
-    @final
-    @property
-    def has_duplicates(self) -> bool:
-        
-        return not self.is_unique
-
-    @final
-    def is_boolean(self) -> bool:
-        
         return self.inferred_type in ["boolean"]
 
     @final
     def is_integer(self) -> bool:
         
-        return self.inferred_type in ["integer"]
-
-    @final
-    def is_floating(self) -> bool:
-        
-        return self.inferred_type in ["floating", "mixed-integer-float", "integer-na"]
-
-    @final
-    def is_numeric(self) -> bool:
-        
-        return self.inferred_type in ["integer", "floating"]
-
-    @final
-    def is_object(self) -> bool:
-        
-        return is_object_dtype(self.dtype)
-
-    @final
-    def is_categorical(self) -> bool:
-        
-        return self.inferred_type in ["categorical"]
-
-    @final
-    def is_interval(self) -> bool:
-        
-        return self.inferred_type in ["interval"]
-
-    @final
-    def is_mixed(self) -> bool:
-        
         warnings.warn(
-            "Index.is_mixed is deprecated and will be removed in a future version. "
-            "Check index.inferred_type directly instead.",
+            f"{type(self).__name__}.is_integer is deprecated. "
+            "Use pandas.api.types.is_integer_dtype instead.",
             FutureWarning,
             stacklevel=find_stack_level(),
         )
-        return self.inferred_type in ["mixed"]
+        return self.inferred_type in ["integer"]
+
+    @final
+    def is_floating(self) -> bool:
+        
+        warnings.warn(
+            f"{type(self).__name__}.is_floating is deprecated. "
+            "Use pandas.api.types.is_float_dtype instead.",
+            FutureWarning,
+            stacklevel=find_stack_level(),
+        )
+        return self.inferred_type in ["floating", "mixed-integer-float", "integer-na"]
+
+    @final
+    def is_numeric(self) -> bool:
+        
+        warnings.warn(
+            f"{type(self).__name__}.is_numeric is deprecated. "
+            "Use pandas.api.types.is_any_real_numeric_dtype instead",
+            FutureWarning,
+            stacklevel=find_stack_level(),
+        )
+        return self.inferred_type in ["integer", "floating"]
+
+    @final
+    def is_object(self) -> bool:
+        
+        warnings.warn(
+            f"{type(self).__name__}.is_object is deprecated."
+            "Use pandas.api.types.is_object_dtype instead",
+            FutureWarning,
+            stacklevel=find_stack_level(),
+        )
+        return is_object_dtype(self.dtype)
+
+    @final
+    def is_categorical(self) -> bool:
+        
+        warnings.warn(
+            f"{type(self).__name__}.is_categorical is deprecated."
+            "Use pandas.api.types.is_categorical_dtype instead",
+            FutureWarning,
+            stacklevel=find_stack_level(),
+        )
+
+        return self.inferred_type in ["categorical"]
+
+    @final
+    def is_interval(self) -> bool:
+        
+        warnings.warn(
+            f"{type(self).__name__}.is_interval is deprecated."
+            "Use pandas.api.types.is_interval_dtype instead",
+            FutureWarning,
+            stacklevel=find_stack_level(),
+        )
+        return self.inferred_type in ["interval"]
+
+    @final
+    def _holds_integer(self) -> bool:
+        
+        return self.inferred_type in ["integer", "mixed-integer"]
 
     @final
     def holds_integer(self) -> bool:
         
-        return self.inferred_type in ["integer", "mixed-integer"]
+        warnings.warn(
+            f"{type(self).__name__}.holds_integer is deprecated. "
+            "Use pandas.api.types.infer_dtype instead.",
+            FutureWarning,
+            stacklevel=find_stack_level(),
+        )
+        return self._holds_integer()
 
     @cache_readonly
     def inferred_type(self) -> str_t:
@@ -1485,18 +1385,6 @@
         elif self._is_multi:
             return False
         return is_datetime_array(ensure_object(self._values))
-
-    @cache_readonly
-    @final
-    def is_all_dates(self) -> bool:
-        
-        warnings.warn(
-            "Index.is_all_dates is deprecated, will be removed in a future version. "
-            "check index.inferred_type instead.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-        return self._is_all_dates
 
     @final
     @cache_readonly
@@ -1566,6 +1454,7 @@
             if downcast is None:
 
 
+
                 return Index._with_infer(result, name=self.name)
             raise NotImplementedError(
                 f"{type(self).__name__}.fillna does not support 'downcast' "
@@ -1573,7 +1462,7 @@
             )
         return self._view()
 
-    def dropna(self: _IndexT, how: str_t = "any") -> _IndexT:
+    def dropna(self: _IndexT, how: AnyAll = "any") -> _IndexT:
         
         if how not in ("any", "all"):
             raise ValueError(f"invalid how option: {how}")
@@ -1597,17 +1486,14 @@
         result = super().unique()
         return self._shallow_copy(result)
 
-    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
-    def drop_duplicates(self: _IndexT, keep: str_t | bool = "first") -> _IndexT:
+    def drop_duplicates(self: _IndexT, *, keep: DropKeep = "first") -> _IndexT:
         
         if self.is_unique:
             return self._view()
 
         return super().drop_duplicates(keep=keep)
 
-    def duplicated(
-        self, keep: Literal["first", "last", False] = "first"
-    ) -> npt.NDArray[np.bool_]:
+    def duplicated(self, keep: DropKeep = "first") -> npt.NDArray[np.bool_]:
         
         if self.is_unique:
 
@@ -1620,39 +1506,6 @@
     def __iadd__(self, other):
 
         return self + other
-
-    @final
-    def __and__(self, other):
-        warnings.warn(
-            "Index.__and__ operating as a set operation is deprecated, "
-            "in the future this will be a logical operation matching "
-            "Series.__and__.  Use index.intersection(other) instead.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-        return self.intersection(other)
-
-    @final
-    def __or__(self, other):
-        warnings.warn(
-            "Index.__or__ operating as a set operation is deprecated, "
-            "in the future this will be a logical operation matching "
-            "Series.__or__.  Use index.union(other) instead.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-        return self.union(other)
-
-    @final
-    def __xor__(self, other):
-        warnings.warn(
-            "Index.__xor__ operating as a set operation is deprecated, "
-            "in the future this will be a logical operation matching "
-            "Series.__xor__.  Use index.symmetric_difference(other) instead.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-        return self.symmetric_difference(other)
 
     @final
     def __nonzero__(self) -> NoReturn:
@@ -1675,14 +1528,14 @@
 
     @final
     def _validate_sort_keyword(self, sort):
-        if sort not in [None, False]:
+        if sort not in [None, False, True]:
             raise ValueError(
                 "The 'sort' keyword only takes the values of "
-                f"None or False; {sort} was passed."
+                f"None, True, or False; {sort} was passed."
             )
 
     @final
-    def _deprecate_dti_setop(self, other: Index, setop: str_t):
+    def _dti_setop_align_tzs(self, other: Index, setop: str_t) -> tuple[Index, Index]:
         
 
 
@@ -1693,14 +1546,10 @@
             and other.tz is not None
         ):
 
-            warnings.warn(
-                f"In a future version, the {setop} of DatetimeIndex objects "
-                "with mismatched timezones will cast both to UTC instead of "
-                "object dtype. To retain the old behavior, "
-                f"use `index.astype(object).{setop}(other)`",
-                FutureWarning,
-                stacklevel=find_stack_level(),
-            )
+            left = self.tz_convert("UTC")
+            right = other.tz_convert("UTC")
+            return left, right
+        return self, other
 
     @final
     def union(self, other, sort=None):
@@ -1712,14 +1561,14 @@
         if not is_dtype_equal(self.dtype, other.dtype):
             if (
                 isinstance(self, ABCMultiIndex)
-                and not is_object_dtype(unpack_nested_dtype(other))
+                and not is_object_dtype(_unpack_nested_dtype(other))
                 and len(other) > 0
             ):
                 raise NotImplementedError(
                     "Can only union MultiIndex with MultiIndex or Index of tuples, "
                     "try mi.to_flat_index().union(other) instead."
                 )
-            self._deprecate_dti_setop(other, "union")
+            self, other = self._dti_setop_align_tzs(other, "union")
 
             dtype = self._find_common_type_compat(other)
             left = self.astype(dtype, copy=False)
@@ -1729,10 +1578,16 @@
         elif not len(other) or self.equals(other):
 
 
-            return self._get_reconciled_name_object(other)
+            result = self._get_reconciled_name_object(other)
+            if sort is True:
+                return result.sort_values()
+            return result
 
         elif not len(self):
-            return other._get_reconciled_name_object(self)
+            result = other._get_reconciled_name_object(self)
+            if sort is True:
+                return result.sort_values()
+            return result
 
         result = self._union(other, sort=sort)
 
@@ -1767,8 +1622,10 @@
 
         elif not other.is_unique:
 
-            result = algos.union_with_duplicates(lvals, rvals)
-            return _maybe_try_sort(result, sort)
+            result_dups = algos.union_with_duplicates(self, other)
+            return _maybe_try_sort(result_dups, sort)
+
+
 
 
 
@@ -1778,11 +1635,17 @@
         else:
             missing = algos.unique1d(self.get_indexer_non_unique(other)[1])
 
-        if len(missing) > 0:
-            other_diff = rvals.take(missing)
-            result = concat_compat((lvals, other_diff))
-        else:
-            result = lvals
+        result: Index | MultiIndex | ArrayLike
+        if self._is_multi:
+
+            result = self.append(other.take(missing))
+
+        else:
+            if len(missing) > 0:
+                other_diff = rvals.take(missing)
+                result = concat_compat((lvals, other_diff))
+            else:
+                result = lvals
 
         if not self.is_monotonic_increasing or not other.is_monotonic_increasing:
 
@@ -1801,19 +1664,23 @@
         return result
 
     @final
-    def intersection(self, other, sort=False):
+    def intersection(self, other, sort: bool = False):
         
         self._validate_sort_keyword(sort)
         self._assert_can_do_setop(other)
         other, result_name = self._convert_can_do_setop(other)
 
         if not is_dtype_equal(self.dtype, other.dtype):
-            self._deprecate_dti_setop(other, "intersection")
+            self, other = self._dti_setop_align_tzs(other, "intersection")
 
         if self.equals(other):
             if self.has_duplicates:
-                return self.unique()._get_reconciled_name_object(other)
-            return self._get_reconciled_name_object(other)
+                result = self.unique()._get_reconciled_name_object(other)
+            else:
+                result = self._get_reconciled_name_object(other)
+            if sort is True:
+                result = result.sort_values()
+            return result
 
         if len(self) == 0 or len(other) == 0:
 
@@ -1854,21 +1721,28 @@
         result = self._intersection(other, sort=sort)
         return self._wrap_intersection_result(other, result)
 
-    def _intersection(self, other: Index, sort=False):
+    def _intersection(self, other: Index, sort: bool = False):
         
         if (
             self.is_monotonic_increasing
             and other.is_monotonic_increasing
             and self._can_use_libjoin
+            and not isinstance(self, ABCMultiIndex)
         ):
             try:
-                result = self._inner_indexer(other)[0]
+                res_indexer, indexer, _ = self._inner_indexer(other)
             except TypeError:
 
                 pass
             else:
 
-                res = algos.unique1d(result)
+                if is_numeric_dtype(self):
+
+
+                    res = algos.unique1d(res_indexer)
+                else:
+                    result = self.take(indexer)
+                    res = result.drop_duplicates()
                 return ensure_wrapped_if_datetimelike(res)
 
         res_values = self._intersection_via_get_indexer(other, sort=sort)
@@ -1880,7 +1754,9 @@
         return self._wrap_setop_result(other, result)
 
     @final
-    def _intersection_via_get_indexer(self, other: Index, sort) -> ArrayLike:
+    def _intersection_via_get_indexer(
+        self, other: Index | MultiIndex, sort
+    ) -> ArrayLike | MultiIndex:
         
         left_unique = self.unique()
         right_unique = other.unique()
@@ -1896,7 +1772,10 @@
 
             taker = np.sort(taker)
 
-        result = left_unique.take(taker)._values
+        if isinstance(left_unique, ABCMultiIndex):
+            result = left_unique.take(taker)
+        else:
+            result = left_unique.take(taker)._values
         return result
 
     @final
@@ -1916,11 +1795,17 @@
 
         if len(other) == 0:
 
-            return self.rename(result_name)
+            result = self.rename(result_name)
+            if sort is True:
+                return result.sort_values()
+            return result
 
         if not self._should_compare(other):
 
-            return self.rename(result_name)
+            result = self.rename(result_name)
+            if sort is True:
+                return result.sort_values()
+            return result
 
         result = self._difference(other, sort=sort)
         return self._wrap_difference_result(other, result)
@@ -1934,7 +1819,12 @@
         indexer = indexer.take((indexer != -1).nonzero()[0])
 
         label_diff = np.setdiff1d(np.arange(this.size), indexer, assume_unique=True)
-        the_diff = this._values.take(label_diff)
+
+        the_diff: MultiIndex | ArrayLike
+        if isinstance(this, ABCMultiIndex):
+            the_diff = this.take(label_diff)
+        else:
+            the_diff = this._values.take(label_diff)
         the_diff = _maybe_try_sort(the_diff, sort)
 
         return the_diff
@@ -1952,7 +1842,7 @@
             result_name = result_name_update
 
         if not is_dtype_equal(self.dtype, other.dtype):
-            self._deprecate_dti_setop(other, "symmetric_difference")
+            self, other = self._dti_setop_align_tzs(other, "symmetric_difference")
 
         if not self._should_compare(other):
             return self.union(other, sort=sort).rename(result_name)
@@ -1972,31 +1862,23 @@
         left_indexer = np.setdiff1d(
             np.arange(this.size), common_indexer, assume_unique=True
         )
-        left_diff = this._values.take(left_indexer)
+        left_diff = this.take(left_indexer)
 
 
         right_indexer = (indexer == -1).nonzero()[0]
-        right_diff = other._values.take(right_indexer)
-
-        res_values = concat_compat([left_diff, right_diff])
-        res_values = _maybe_try_sort(res_values, sort)
-
-
-        result = Index(res_values, name=result_name, dtype=res_values.dtype)
-
-        if self._is_multi:
-            self = cast("MultiIndex", self)
+        right_diff = other.take(right_indexer)
+
+        res_values = left_diff.append(right_diff)
+        result = _maybe_try_sort(res_values, sort)
+
+        if not self._is_multi:
+            return Index(result, name=result_name, dtype=res_values.dtype)
+        else:
+            left_diff = cast("MultiIndex", left_diff)
             if len(result) == 0:
 
-
-                return type(self)(
-                    levels=[[] for _ in range(self.nlevels)],
-                    codes=[[] for _ in range(self.nlevels)],
-                    names=result.name,
-                )
-            return type(self).from_tuples(result, names=result.name)
-
-        return result
+                return left_diff.remove_unused_levels().set_names(result_name)
+            return result.set_names(result_name)
 
     @final
     def _assert_can_do_setop(self, other) -> bool:
@@ -2006,13 +1888,7 @@
 
     def _convert_can_do_setop(self, other) -> tuple[Index, Hashable]:
         if not isinstance(other, Index):
-
-
-            if hasattr(other, "dtype"):
-                other = Index(other, name=self.name, dtype=other.dtype)
-            else:
-
-                other = Index(other, name=self.name)
+            other = Index(other, name=self.name)
             result_name = self.name
         else:
             result_name = get_op_result_name(self, other)
@@ -2021,48 +1897,19 @@
 
 
 
-    def get_loc(self, key, method=None, tolerance=None):
-        
-        if method is None:
-            if tolerance is not None:
-                raise ValueError(
-                    "tolerance argument only valid if using pad, "
-                    "backfill or nearest lookups"
-                )
-            casted_key = self._maybe_cast_indexer(key)
-            try:
-                return self._engine.get_loc(casted_key)
-            except KeyError as err:
-                raise KeyError(key) from err
-            except TypeError:
-
-
-
-                self._check_indexing_error(key)
-                raise
-
-
-        warnings.warn(
-            f"Passing method to {type(self).__name__}.get_loc is deprecated "
-            "and will raise in a future version. Use "
-            "index.get_indexer([item], method=...) instead.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-
-        if is_scalar(key) and isna(key) and not self.hasnans:
-            raise KeyError(key)
-
-        if tolerance is not None:
-            tolerance = self._convert_tolerance(tolerance, np.asarray(key))
-
-        indexer = self.get_indexer([key], method=method, tolerance=tolerance)
-        if indexer.ndim > 1 or indexer.size > 1:
-            raise TypeError("get_loc requires scalar valued input")
-        loc = indexer.item()
-        if loc == -1:
-            raise KeyError(key)
-        return loc
+    def get_loc(self, key):
+        
+        casted_key = self._maybe_cast_indexer(key)
+        try:
+            return self._engine.get_loc(casted_key)
+        except KeyError as err:
+            raise KeyError(key) from err
+        except TypeError:
+
+
+
+            self._check_indexing_error(key)
+            raise
 
     _index_shared_docs[
         "get_indexer"
@@ -2097,7 +1944,7 @@
 
         Returns
         -------
-        indexer : np.ndarray[np.intp]
+        np.ndarray[np.intp]
             Integers from 0 to n - 1 indicating that the index at these
             positions matches the corresponding target values. Missing values
             in the target are marked by -1.
@@ -2126,7 +1973,7 @@
         limit: int | None = None,
         tolerance=None,
     ) -> npt.NDArray[np.intp]:
-        method = missing.clean_reindex_fill_method(method)
+        method = clean_reindex_fill_method(method)
         orig_target = target
         target = self._maybe_cast_listlike_indexer(target)
 
@@ -2190,9 +2037,10 @@
 
             return np.arange(len(target), dtype=np.intp)
 
-        if not is_dtype_equal(self.dtype, target.dtype) and not is_interval_dtype(
-            self.dtype
-        ):
+        if not is_dtype_equal(
+            self.dtype, target.dtype
+        ) and not self._should_partial_index(target):
+
 
             dtype = self._find_common_type_compat(target)
 
@@ -2266,7 +2114,7 @@
                     "method='nearest' not implemented yet "
                     "for MultiIndex; see GitHub issue 9365"
                 )
-            elif method == "pad" or method == "backfill":
+            if method in ("pad", "backfill"):
                 if tolerance is not None:
                     raise NotImplementedError(
                         "tolerance not implemented yet for MultiIndex"
@@ -2296,21 +2144,37 @@
         tolerance = np.asarray(tolerance)
         if target.size != tolerance.size and tolerance.size > 1:
             raise ValueError("list-like tolerance size must match target index size")
+        elif is_numeric_dtype(self) and not np.issubdtype(tolerance.dtype, np.number):
+            if tolerance.ndim > 0:
+                raise ValueError(
+                    f"tolerance argument for {type(self).__name__} with dtype "
+                    f"{self.dtype} must contain numeric elements if it is list type"
+                )
+
+            raise ValueError(
+                f"tolerance argument for {type(self).__name__} with dtype {self.dtype} "
+                f"must be numeric if it is a scalar: {repr(tolerance)}"
+            )
         return tolerance
 
     @final
     def _get_fill_indexer(
         self, target: Index, method: str_t, limit: int | None = None, tolerance=None
     ) -> npt.NDArray[np.intp]:
-
         if self._is_multi:
 
 
 
             engine = self._engine
-            return engine.get_indexer_with_fill(
-                target=target._values, values=self._values, method=method, limit=limit
-            )
+            with warnings.catch_warnings():
+
+                warnings.filterwarnings("ignore", category=RuntimeWarning)
+                return engine.get_indexer_with_fill(
+                    target=target._values,
+                    values=self._values,
+                    method=method,
+                    limit=limit,
+                )
 
         if self.is_monotonic_increasing and target.is_monotonic_increasing:
             target_values = target._get_engine_target()
@@ -2397,7 +2261,6 @@
         indexer: npt.NDArray[np.intp],
         tolerance,
     ) -> npt.NDArray[np.intp]:
-
         distance = self._difference_compat(target, indexer)
 
         return np.where(distance <= tolerance, indexer, -1)
@@ -2436,6 +2299,13 @@
 
 
         start, stop, step = key.start, key.stop, key.step
+
+
+
+        if isinstance(self.dtype, np.dtype) and is_float_dtype(self.dtype):
+
+
+            return self.slice_indexer(start, stop, step)
 
 
         def is_int(v):
@@ -2453,7 +2323,7 @@
 
         if kind == "getitem":
 
-            if self.is_integer() or is_index_slice:
+            if is_integer_dtype(self.dtype) or is_index_slice:
 
                 self._validate_indexer("slice", key.start, "getitem")
                 self._validate_indexer("slice", key.stop, "getitem")
@@ -2480,12 +2350,9 @@
         elif is_positional:
             if kind == "loc":
 
-                warnings.warn(
-                    "Slicing a positional slice with .loc is not supported, "
-                    "and will raise TypeError in a future version.  "
+                raise TypeError(
+                    "Slicing a positional slice with .loc is not allowed, "
                     "Use .loc with labels or .iloc with positions instead.",
-                    FutureWarning,
-                    stacklevel=find_stack_level(),
                 )
             indexer = key
         else:
@@ -2494,12 +2361,20 @@
         return indexer
 
     @final
-    def _invalid_indexer(self, form: str_t, key) -> TypeError:
-        
-        return TypeError(
+    def _raise_invalid_indexer(
+        self,
+        form: str_t,
+        key,
+        reraise: lib.NoDefault | None | Exception = lib.no_default,
+    ) -> None:
+        
+        msg = (
             f"cannot do {form} indexing on {type(self).__name__} with these "
             f"indexers [{key}] of type {type(key).__name__}"
         )
+        if reraise is not lib.no_default:
+            raise TypeError(msg) from reraise
+        raise TypeError(msg)
 
 
 
@@ -2554,22 +2429,11 @@
                     )
                 elif self._is_multi:
                     raise ValueError("cannot handle a non-unique multi-index!")
+                elif not self.is_unique:
+
+                    raise ValueError("cannot reindex on an axis with duplicate labels")
                 else:
-                    if method is not None or limit is not None:
-                        raise ValueError(
-                            "cannot reindex a non-unique index "
-                            "with a method or limit"
-                        )
                     indexer, _ = self.get_indexer_non_unique(target)
-
-                if not self.is_unique:
-
-                    warnings.warn(
-                        "reindexing with a non-unique Index is deprecated and "
-                        "will raise in a future version.",
-                        FutureWarning,
-                        stacklevel=find_stack_level(),
-                    )
 
         target = self._wrap_reindex_result(target, indexer, preserve_names)
         return target, indexer
@@ -2615,12 +2479,10 @@
 
 
             if not len(self):
-
                 new_indexer = np.arange(0, dtype=np.intp)
 
 
             elif target.is_unique:
-
 
                 new_indexer = np.arange(len(indexer), dtype=np.intp)
                 new_indexer[cur_indexer] = np.arange(len(cur_labels))
@@ -2630,17 +2492,16 @@
 
             else:
 
-
                 indexer[~check] = -1
 
 
                 new_indexer = np.arange(len(self.take(indexer)), dtype=np.intp)
                 new_indexer[~check] = -1
 
-        if isinstance(self, ABCMultiIndex):
+        if not isinstance(self, ABCMultiIndex):
+            new_index = Index(new_labels, name=self.name)
+        else:
             new_index = type(self).from_tuples(new_labels, names=self.names)
-        else:
-            new_index = Index._with_infer(new_labels, name=self.name)
         return new_index, indexer, new_indexer
 
 
@@ -2651,7 +2512,7 @@
         self,
         other: Index,
         *,
-        how: str_t = ...,
+        how: JoinHow = ...,
         level: Level = ...,
         return_indexers: Literal[True],
         sort: bool = ...,
@@ -2663,7 +2524,7 @@
         self,
         other: Index,
         *,
-        how: str_t = ...,
+        how: JoinHow = ...,
         level: Level = ...,
         return_indexers: Literal[False] = ...,
         sort: bool = ...,
@@ -2675,7 +2536,7 @@
         self,
         other: Index,
         *,
-        how: str_t = ...,
+        how: JoinHow = ...,
         level: Level = ...,
         return_indexers: bool = ...,
         sort: bool = ...,
@@ -2683,12 +2544,12 @@
         ...
 
     @final
-    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "other"])
     @_maybe_return_indexers
     def join(
         self,
         other: Index,
-        how: str_t = "left",
+        *,
+        how: JoinHow = "left",
         level: Level = None,
         return_indexers: bool = False,
         sort: bool = False,
@@ -2715,7 +2576,6 @@
 
 
         if level is None and (self._is_multi or other._is_multi):
-
 
             if self.names == other.names:
                 pass
@@ -2747,7 +2607,8 @@
                 return join_index, None, rindexer
 
         if self._join_precedence < other._join_precedence:
-            how = {"right": "left", "left": "right"}.get(how, how)
+            flip: dict[JoinHow, JoinHow] = {"right": "left", "left": "right"}
+            how = flip.get(how, how)
             join_index, lidx, ridx = other.join(
                 self, how=how, level=level, return_indexers=True
             )
@@ -2774,13 +2635,11 @@
             else:
                 return self._join_non_unique(other, how=how)
         elif (
+
             self.is_monotonic_increasing
             and other.is_monotonic_increasing
             and self._can_use_libjoin
-            and (
-                not isinstance(self, ABCMultiIndex)
-                or not any(is_categorical_dtype(dtype) for dtype in self.dtypes)
-            )
+            and not isinstance(self, ABCMultiIndex)
             and not is_categorical_dtype(self.dtype)
         ):
 
@@ -2795,7 +2654,7 @@
 
     @final
     def _join_via_get_indexer(
-        self, other: Index, how: str_t, sort: bool
+        self, other: Index, how: JoinHow, sort: bool
     ) -> tuple[Index, npt.NDArray[np.intp] | None, npt.NDArray[np.intp] | None]:
 
 
@@ -2829,7 +2688,7 @@
         return join_index, lindexer, rindexer
 
     @final
-    def _join_multi(self, other: Index, how: str_t):
+    def _join_multi(self, other: Index, how: JoinHow):
         from pandas.core.indexes.multi import MultiIndex
         from pandas.core.reshape.merge import restore_dropped_levels_multijoin
 
@@ -2847,7 +2706,6 @@
             raise ValueError("cannot join with no overlapping index names")
 
         if isinstance(self, MultiIndex) and isinstance(other, MultiIndex):
-
 
             ldrop_names = sorted(self_names - overlap, key=self_names_order)
             rdrop_names = sorted(other_names - overlap, key=other_names_order)
@@ -2901,7 +2759,8 @@
             self, other = other, self
             flip_order = True
 
-            how = {"right": "left", "left": "right"}.get(how, how)
+            flip: dict[JoinHow, JoinHow] = {"right": "left", "left": "right"}
+            how = flip.get(how, how)
 
         level = other.names.index(jl)
         result = self._join_level(other, level, how=how)
@@ -2912,7 +2771,7 @@
 
     @final
     def _join_non_unique(
-        self, other: Index, how: str_t = "left"
+        self, other: Index, how: JoinHow = "left"
     ) -> tuple[Index, npt.NDArray[np.intp], npt.NDArray[np.intp]]:
         from pandas.core.reshape.merge import get_join_indexers
 
@@ -2924,27 +2783,14 @@
         )
         mask = left_idx == -1
 
-        join_array = self._values.take(left_idx)
-        right = other._values.take(right_idx)
-
-        if isinstance(join_array, np.ndarray):
-
-
-
-
-
-
-            np.putmask(join_array, mask, right)
-        else:
-            join_array._putmask(mask, right)
-
-        join_index = self._wrap_joined_index(join_array, other)
-
+        join_idx = self.take(left_idx)
+        right = other.take(right_idx)
+        join_index = join_idx.putmask(mask, right)
         return join_index, left_idx, right_idx
 
     @final
     def _join_level(
-        self, other: Index, level, how: str_t = "left", keep_order: bool = True
+        self, other: Index, level, how: JoinHow = "left", keep_order: bool = True
     ) -> tuple[MultiIndex, npt.NDArray[np.intp] | None, npt.NDArray[np.intp] | None]:
         
         from pandas.core.indexes.multi import MultiIndex
@@ -2975,7 +2821,8 @@
         flip_order = not isinstance(self, MultiIndex)
         if flip_order:
             left, right = right, left
-            how = {"right": "left", "left": "right"}.get(how, how)
+            flip: dict[JoinHow, JoinHow] = {"right": "left", "left": "right"}
+            how = flip.get(how, how)
 
         assert isinstance(left, MultiIndex)
 
@@ -3072,17 +2919,20 @@
 
     @final
     def _join_monotonic(
-        self, other: Index, how: str_t = "left"
+        self, other: Index, how: JoinHow = "left"
     ) -> tuple[Index, npt.NDArray[np.intp] | None, npt.NDArray[np.intp] | None]:
 
         assert other.dtype == self.dtype
 
         if self.equals(other):
+
+
+
             ret_index = other if how == "right" else self
             return ret_index, None, None
 
-        ridx: np.ndarray | None
-        lidx: np.ndarray | None
+        ridx: npt.NDArray[np.intp] | None
+        lidx: npt.NDArray[np.intp] | None
 
         if self.is_unique and other.is_unique:
 
@@ -3096,10 +2946,10 @@
                 ridx = None
             elif how == "inner":
                 join_array, lidx, ridx = self._inner_indexer(other)
-                join_index = self._wrap_joined_index(join_array, other)
+                join_index = self._wrap_joined_index(join_array, other, lidx, ridx)
             elif how == "outer":
                 join_array, lidx, ridx = self._outer_indexer(other)
-                join_index = self._wrap_joined_index(join_array, other)
+                join_index = self._wrap_joined_index(join_array, other, lidx, ridx)
         else:
             if how == "left":
                 join_array, lidx, ridx = self._left_indexer(other)
@@ -3110,20 +2960,33 @@
             elif how == "outer":
                 join_array, lidx, ridx = self._outer_indexer(other)
 
-            join_index = self._wrap_joined_index(join_array, other)
+            assert lidx is not None
+            assert ridx is not None
+
+            join_index = self._wrap_joined_index(join_array, other, lidx, ridx)
 
         lidx = None if lidx is None else ensure_platform_int(lidx)
         ridx = None if ridx is None else ensure_platform_int(ridx)
         return join_index, lidx, ridx
 
-    def _wrap_joined_index(self: _IndexT, joined: ArrayLike, other: _IndexT) -> _IndexT:
+    def _wrap_joined_index(
+        self: _IndexT,
+        joined: ArrayLike,
+        other: _IndexT,
+        lidx: npt.NDArray[np.intp],
+        ridx: npt.NDArray[np.intp],
+    ) -> _IndexT:
         assert other.dtype == self.dtype
 
         if isinstance(self, ABCMultiIndex):
             name = self.names if self.names == other.names else None
 
 
-            return self._constructor(joined, name=name)
+            mask = lidx == -1
+            join_idx = self.take(lidx)
+            right = other.take(ridx)
+            join_index = join_idx.putmask(mask, right)
+            return join_index.set_names(name)
         else:
             name = get_op_result_name(self, other)
             return self._constructor._with_infer(joined, name=name, dtype=self.dtype)
@@ -3133,7 +2996,12 @@
         
         if type(self) is Index:
 
-            return isinstance(self.dtype, np.dtype)
+
+            return (
+                isinstance(self.dtype, np.dtype)
+                or isinstance(self.values, BaseMaskedArray)
+                or isinstance(self._values, ArrowExtensionArray)
+            )
         return not is_interval_dtype(self.dtype)
 
 
@@ -3143,8 +3011,6 @@
     def values(self) -> ArrayLike:
         
         return self._data
-
-
 
     @cache_readonly
     @doc(IndexOpsMixin.array)
@@ -3167,13 +3033,38 @@
         if isinstance(vals, StringArray):
 
             return vals._ndarray
-        if type(self) is Index and isinstance(self._values, ExtensionArray):
+        if (
+            type(self) is Index
+            and isinstance(self._values, ExtensionArray)
+            and not isinstance(self._values, BaseMaskedArray)
+            and not (
+                isinstance(self._values, ArrowExtensionArray)
+                and is_numeric_dtype(self.dtype)
+
+                and self.dtype.kind != "O"
+            )
+        ):
 
             return self._values.astype(object)
         return vals
 
+    def _get_join_target(self) -> ArrayLike:
+        
+        if isinstance(self._values, BaseMaskedArray):
+
+            return self._values._data
+        elif isinstance(self._values, ArrowExtensionArray):
+
+
+            return self._values.to_numpy()
+        return self._get_engine_target()
+
     def _from_join_target(self, result: np.ndarray) -> ArrayLike:
         
+        if isinstance(self.values, BaseMaskedArray):
+            return type(self.values)(result, np.zeros(result.shape, dtype=np.bool_))
+        elif isinstance(self.values, ArrowExtensionArray):
+            return type(self.values)._from_sequence(result)
         return result
 
     @doc(IndexOpsMixin._memory_usage)
@@ -3197,20 +3088,12 @@
 
     @final
     @classmethod
-    def _scalar_data_error(cls, data):
-
-
-        return TypeError(
+    def _raise_scalar_data_error(cls, data):
+
+
+        raise TypeError(
             f"{cls.__name__}(...) must be called with a collection of some "
             f"kind, {repr(data)} was passed"
-        )
-
-    @final
-    @classmethod
-    def _string_data_error(cls, data):
-        raise TypeError(
-            "String dtype not supported, you may need "
-            "to explicitly cast to a numeric type"
         )
 
     def _validate_fill_value(self, value):
@@ -3236,17 +3119,7 @@
 
     def _is_memory_usage_qualified(self) -> bool:
         
-        return self.is_object()
-
-    def is_type_compatible(self, kind: str_t) -> bool:
-        
-        warnings.warn(
-            "Index.is_type_compatible is deprecated and will be removed in a "
-            "future version.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-        return kind == self.inferred_type
+        return is_object_dtype(self.dtype)
 
     def __contains__(self, key: Any) -> bool:
         
@@ -3271,7 +3144,7 @@
 
         if is_integer(key) or is_float(key):
 
-            key = com.cast_scalar_indexer(key, warn_float=True)
+            key = com.cast_scalar_indexer(key)
             return getitem(key)
 
         if isinstance(key, slice):
@@ -3279,7 +3152,9 @@
 
             result = getitem(key)
 
-            return type(self)._simple_new(result, name=self._name)
+            return type(self)._simple_new(
+                result, name=self._name, refs=self._references
+            )
 
         if com.is_bool_indexer(key):
 
@@ -3294,15 +3169,7 @@
         result = getitem(key)
 
         if result.ndim > 1:
-            deprecate_ndim_indexing(result)
-            if hasattr(result, "_ndarray"):
-
-
-
-
-
-                return result._ndarray
-            return result
+            disallow_ndim_indexing(result)
 
 
 
@@ -3311,12 +3178,16 @@
     def _getitem_slice(self: _IndexT, slobj: slice) -> _IndexT:
         
         res = self._data[slobj]
-        return type(self)._simple_new(res, name=self._name)
+        return type(self)._simple_new(res, name=self._name, refs=self._references)
 
     @final
     def _can_hold_identifiers_and_holds_name(self, name) -> bool:
         
-        if self.is_object() or is_string_dtype(self.dtype) or self.is_categorical():
+        if (
+            is_object_dtype(self.dtype)
+            or is_string_dtype(self.dtype)
+            or is_categorical_dtype(self.dtype)
+        ):
             return name in self
         return False
 
@@ -3346,13 +3217,8 @@
 
         result = concat_compat(to_concat_vals)
 
-        is_numeric = result.dtype.kind in ["i", "u", "f"]
-        if self._is_backward_compat_public_numeric_index and is_numeric:
-            return type(self)._simple_new(result, name=name)
-
         return Index._with_infer(result, name=name)
 
-    @final
     def putmask(self, mask, value) -> Index:
         
         mask, noop = validate_putmask(self._values, mask)
@@ -3362,11 +3228,13 @@
         if self.dtype != object and is_valid_na_for_dtype(value, self.dtype):
 
             value = self._na_value
+
         try:
             converted = self._validate_fill_value(value)
         except (LossySetitemError, ValueError, TypeError) as err:
             if is_object_dtype(self):
                 raise err
+
 
             dtype = self._find_common_type_compat(value)
             return self.astype(dtype).putmask(mask, value)
@@ -3424,6 +3292,7 @@
                 for c in self._comparables
             )
             and type(self) == type(other)
+            and self.dtype == other.dtype
         )
 
     @final
@@ -3500,7 +3369,7 @@
         
         raise TypeError("cannot sort an Index object in-place, use sort_values instead")
 
-    def shift(self, periods=1, freq=None):
+    def shift(self, periods: int = 1, freq=None):
         
         raise NotImplementedError(
             f"This method is only implemented for DatetimeIndex, PeriodIndex and "
@@ -3513,37 +3382,6 @@
 
         return self._data.argsort(*args, **kwargs)
 
-    @final
-    def get_value(self, series: Series, key):
-        
-        warnings.warn(
-            "get_value is deprecated and will be removed in a future version. "
-            "Use Series[key] instead.",
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-
-        self._check_indexing_error(key)
-
-        try:
-
-
-
-
-
-            loc = self.get_loc(key)
-        except KeyError:
-            if not self._should_fallback_to_positional:
-                raise
-            elif is_integer(key):
-
-
-                loc = key
-            else:
-                raise
-
-        return self._get_values_for_loc(series, loc, key)
-
     def _check_indexing_error(self, key):
         if not is_scalar(key):
 
@@ -3553,30 +3391,12 @@
     @cache_readonly
     def _should_fallback_to_positional(self) -> bool:
         
-        return not self.holds_integer()
-
-    def _get_values_for_loc(self, series: Series, loc, key):
-        
-        if is_integer(loc):
-            return series._values[loc]
-
-        return series.iloc[loc]
-
-    @final
-    def set_value(self, arr, key, value) -> None:
-        
-        warnings.warn(
-            (
-                "The 'set_value' method is deprecated, and "
-                "will be removed in a future version."
-            ),
-            FutureWarning,
-            stacklevel=find_stack_level(),
-        )
-        loc = self._engine.get_loc(key)
-        if not can_hold_element(arr, value):
-            raise ValueError
-        arr[loc] = value
+        return self.inferred_type not in {
+            "integer",
+            "mixed-integer",
+            "floating",
+            "complex",
+        }
 
     _index_shared_docs[
         "get_indexer_non_unique"
@@ -3599,6 +3419,31 @@
         missing : np.ndarray[np.intp]
             An indexer into the target of the values not found.
             These correspond to the -1 in the indexer array.
+
+        Examples
+        --------
+        >>> index = pd.Index(['c', 'b', 'a', 'b', 'b'])
+        >>> index.get_indexer_non_unique(['b', 'b'])
+        (array([1, 3, 4, 1, 3, 4]), array([], dtype=int64))
+
+        In the example below there are no matched values.
+
+        >>> index = pd.Index(['c', 'b', 'a', 'b', 'b'])
+        >>> index.get_indexer_non_unique(['q', 'r', 't'])
+        (array([-1, -1, -1]), array([0, 1, 2]))
+
+        For this reason, the returned ``indexer`` contains only integers equal to -1.
+        It demonstrates that there's no match between the index and the ``target``
+        values at these positions. The mask [0, 1, 2] in the return value shows that
+        the first, second, and third elements are missing.
+
+        Notice that the return value is a tuple contains two items. In the example
+        below the first item is an array of locations in ``index``. The second
+        item is a mask shows that the first and third elements are missing.
+
+        >>> index = pd.Index(['c', 'b', 'a', 'b', 'b'])
+        >>> index.get_indexer_non_unique(['f', 'b', 's'])
+        (array([-1,  1,  3,  4, -1]), array([0, 2]))
         """
 
     @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
@@ -3608,7 +3453,7 @@
         target = ensure_index(target)
         target = self._maybe_cast_listlike_indexer(target)
 
-        if not self._should_compare(target) and not is_interval_dtype(self.dtype):
+        if not self._should_compare(target) and not self._should_partial_index(target):
 
 
             return self._get_indexer_non_comparable(target, method=None, unique=False)
@@ -3625,6 +3470,9 @@
             this = self.astype(dtype, copy=False)
             that = target.astype(dtype, copy=False)
             return this.get_indexer_non_unique(that)
+
+
+
 
 
 
@@ -3685,7 +3533,6 @@
         nmissing = missing_mask.sum()
 
         if nmissing:
-
 
 
             use_interval_msg = is_interval_dtype(self.dtype) or (
@@ -3728,7 +3575,7 @@
     ) -> npt.NDArray[np.intp] | tuple[npt.NDArray[np.intp], npt.NDArray[np.intp]]:
         
         if method is not None:
-            other = unpack_nested_dtype(target)
+            other = _unpack_nested_dtype(target)
             raise TypeError(f"Cannot compare dtypes {self.dtype} and {other.dtype}")
 
         no_matches = -1 * np.ones(target.shape, dtype=np.intp)
@@ -3793,16 +3640,6 @@
     @final
     def _find_common_type_compat(self, target) -> DtypeObj:
         
-        if is_valid_na_for_dtype(target, self.dtype):
-
-            dtype = ensure_dtype_can_hold_na(self.dtype)
-            if is_dtype_equal(self.dtype, dtype):
-                raise NotImplementedError(
-                    "This should not be reached. Please report a bug at "
-                    "github.com/pandas-dev/pandas"
-                )
-            return dtype
-
         target_dtype, _ = infer_dtype_from(target, pandas_dtype=True)
 
 
@@ -3817,7 +3654,7 @@
             ):
                 return _dtype_obj
 
-        dtype = find_common_type([self.dtype, target_dtype])
+        dtype = find_result_type(self._values, target)
         dtype = common_dtype_categorical_compat([self, target], dtype)
         return dtype
 
@@ -3825,15 +3662,15 @@
     def _should_compare(self, other: Index) -> bool:
         
 
-        if (other.is_boolean() and self.is_numeric()) or (
-            self.is_boolean() and other.is_numeric()
+        if (is_bool_dtype(other) and is_any_real_numeric_dtype(self)) or (
+            is_bool_dtype(self) and is_any_real_numeric_dtype(other)
         ):
 
 
 
             return False
 
-        other = unpack_nested_dtype(other)
+        other = _unpack_nested_dtype(other)
         dtype = other.dtype
         return self._is_comparable_dtype(dtype) or is_object_dtype(dtype)
 
@@ -3843,6 +3680,8 @@
             return dtype.kind == "b"
         elif is_numeric_dtype(self.dtype):
             return is_numeric_dtype(dtype)
+
+
         return True
 
     @final
@@ -3890,13 +3729,6 @@
                 new_values, self.dtype, same_dtype=same_dtype
             )
 
-        if self._is_backward_compat_public_numeric_index and is_numeric_dtype(
-            new_values.dtype
-        ):
-            return self._constructor(
-                new_values, dtype=dtype, copy=False, name=self.name
-            )
-
         return Index._with_infer(new_values, dtype=dtype, copy=False, name=self.name)
 
 
@@ -3904,15 +3736,13 @@
     def _transform_index(self, func, *, level=None) -> Index:
         
         if isinstance(self, ABCMultiIndex):
-            if level is not None:
-
-                items = [
-                    tuple(func(y) if i == level else y for i, y in enumerate(x))
-                    for x in self
-                ]
-            else:
-                items = [tuple(func(y) for y in x) for x in self]
-            return type(self).from_tuples(items, names=self.names)
+            values = [
+                self.get_level_values(i).map(func)
+                if i == level or level is None
+                else self.get_level_values(i)
+                for i in range(self.nlevels)
+            ]
+            return type(self).from_arrays(values)
         else:
             items = [func(x) for x in self]
             return Index(items, name=self.name, tupleize_cols=False)
@@ -3933,11 +3763,8 @@
         start: Hashable | None = None,
         end: Hashable | None = None,
         step: int | None = None,
-        kind=no_default,
     ) -> slice:
         
-        self._deprecated_arg(kind, "kind", "slice_indexer")
-
         start_slice, end_slice = self.slice_locs(start, end, step=step)
 
 
@@ -3957,24 +3784,25 @@
         return ensure_index(target)
 
     @final
-    def _validate_indexer(self, form: str_t, key, kind: str_t):
+    def _validate_indexer(self, form: str_t, key, kind: str_t) -> None:
         
         assert kind in ["getitem", "iloc"]
 
         if key is not None and not is_integer(key):
-            raise self._invalid_indexer(form, key)
-
-    def _maybe_cast_slice_bound(self, label, side: str_t, kind=no_default):
-        
-        assert kind in ["loc", "getitem", None, no_default]
-        self._deprecated_arg(kind, "kind", "_maybe_cast_slice_bound")
-
-
-
+            self._raise_invalid_indexer(form, key)
+
+    def _maybe_cast_slice_bound(self, label, side: str_t):
+        
+
+
+
+
+        if is_numeric_dtype(self.dtype):
+            return self._maybe_cast_indexer(label)
 
 
         if (is_float(label) or is_integer(label)) and label not in self:
-            raise self._invalid_indexer("slice", label)
+            self._raise_invalid_indexer("slice", label)
 
         return label
 
@@ -3992,12 +3820,8 @@
 
         raise ValueError("index must be monotonic increasing or decreasing")
 
-    def get_slice_bound(
-        self, label, side: Literal["left", "right"], kind=no_default
-    ) -> int:
-        
-        assert kind in ["loc", "getitem", None, no_default]
-        self._deprecated_arg(kind, "kind", "get_slice_bound")
+    def get_slice_bound(self, label, side: Literal["left", "right"]) -> int:
+        
 
         if side not in ("left", "right"):
             raise ValueError(
@@ -4043,11 +3867,8 @@
             else:
                 return slc
 
-    def slice_locs(
-        self, start=None, end=None, step=None, kind=no_default
-    ) -> tuple[int, int]:
-        
-        self._deprecated_arg(kind, "kind", "slice_locs")
+    def slice_locs(self, start=None, end=None, step=None) -> tuple[int, int]:
+        
         inc = step is None or step >= 0
 
         if not inc:
@@ -4155,12 +3976,7 @@
             loc = loc if loc >= 0 else loc - 1
             new_values[loc] = item
 
-        if self._typ == "numericindex":
-
-
-            return self._constructor._with_infer(new_values, name=self.name)
-        else:
-            return Index._with_infer(new_values, name=self.name)
+        return Index._with_infer(new_values, name=self.name)
 
     def drop(
         self,
@@ -4181,6 +3997,33 @@
             indexer = indexer[~mask]
         return self.delete(indexer)
 
+    def infer_objects(self, copy: bool = True) -> Index:
+        
+        if self._is_multi:
+            raise NotImplementedError(
+                "infer_objects is not implemented for MultiIndex. "
+                "Use index.to_frame().infer_objects() instead."
+            )
+        if self.dtype != object:
+            return self.copy() if copy else self
+
+        values = self._values
+        values = cast("npt.NDArray[np.object_]", values)
+        res_values = lib.maybe_convert_objects(
+            values,
+            convert_datetime=True,
+            convert_timedelta=True,
+            convert_period=True,
+            convert_interval=True,
+        )
+        if copy and res_values is values:
+            return self.copy()
+        result = Index(res_values, name=self.name)
+        if not copy and res_values is values and self._references is not None:
+            result._references = self._references
+            result._references.add_index_reference(result)
+        return result
+
 
 
 
@@ -4229,13 +4072,24 @@
 
         return result
 
+    @final
+    def _logical_method(self, other, op):
+        res_name = ops.get_op_result_name(self, other)
+
+        lvalues = self._values
+        rvalues = extract_array(other, extract_numpy=True, extract_range=True)
+
+        res_values = ops.logical_op(lvalues, rvalues, op)
+        return self._construct_result(res_values, name=res_name)
+
+    @final
     def _construct_result(self, result, name):
         if isinstance(result, tuple):
             return (
-                Index._with_infer(result[0], name=name),
-                Index._with_infer(result[1], name=name),
+                Index(result[0], name=name, dtype=result[0].dtype),
+                Index(result[1], name=name, dtype=result[1].dtype),
             )
-        return Index._with_infer(result, name=name)
+        return Index(result, name=name, dtype=result.dtype)
 
     def _arith_method(self, other, op):
         if (
@@ -4305,7 +4159,7 @@
             make_invalid_op(opname)(self)
 
     @Appender(IndexOpsMixin.argmin.__doc__)
-    def argmin(self, axis=None, skipna=True, *args, **kwargs) -> int:
+    def argmin(self, axis=None, skipna: bool = True, *args, **kwargs) -> int:
         nv.validate_argmin(args, kwargs)
         nv.validate_minmax_axis(axis)
 
@@ -4317,7 +4171,7 @@
         return super().argmin(skipna=skipna)
 
     @Appender(IndexOpsMixin.argmax.__doc__)
-    def argmax(self, axis=None, skipna=True, *args, **kwargs) -> int:
+    def argmax(self, axis=None, skipna: bool = True, *args, **kwargs) -> int:
         nv.validate_argmax(args, kwargs)
         nv.validate_minmax_axis(axis)
 
@@ -4329,7 +4183,7 @@
         return super().argmax(skipna=skipna)
 
     @doc(IndexOpsMixin.min)
-    def min(self, axis=None, skipna=True, *args, **kwargs):
+    def min(self, axis=None, skipna: bool = True, *args, **kwargs):
         nv.validate_min(args, kwargs)
         nv.validate_minmax_axis(axis)
 
@@ -4349,13 +4203,12 @@
                 return self._na_value
 
         if not self._is_multi and not isinstance(self._values, np.ndarray):
-
-            return self._values.min(skipna=skipna)
+            return self._values._reduce(name="min", skipna=skipna)
 
         return super().min(skipna=skipna)
 
     @doc(IndexOpsMixin.max)
-    def max(self, axis=None, skipna=True, *args, **kwargs):
+    def max(self, axis=None, skipna: bool = True, *args, **kwargs):
         nv.validate_max(args, kwargs)
         nv.validate_minmax_axis(axis)
 
@@ -4375,8 +4228,7 @@
                 return self._na_value
 
         if not self._is_multi and not isinstance(self._values, np.ndarray):
-
-            return self._values.max(skipna=skipna)
+            return self._values._reduce(name="max", skipna=skipna)
 
         return super().max(skipna=skipna)
 
@@ -4388,14 +4240,3 @@
         
 
         return (len(self),)
-
-    @final
-    def _deprecated_arg(self, value, name: str_t, methodname: str_t) -> None:
-        
-        if value is not no_default:
-            warnings.warn(
-                f"'{name}' argument in {methodname} is deprecated "
-                "and will be removed in a future version.  Do not pass it.",
-                FutureWarning,
-                stacklevel=find_stack_level(),
-            )
```

```json
{
  "old_file": "R_candidates/Vi-1_v1.5.3/pandas.core.indexes.base.Index.py",
  "new_file": "R_candidates/Vi_v2.0.0/pandas.core.indexes.base.Index.py",
  "lines_added": 695,
  "lines_removed": 854
}
```
