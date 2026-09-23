# 一、突变情况分析

- **Total**: 457
- **替代API**: `polars.expr.expr.Expr.replace`
- **10% 阈值**: 45.7

## Vi-1 (py-0.19.15-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 457 | 0.2764 |
| tokenBased | 3 | 0.2723 |
| treeBased | 3 | 0.3026 |

## Vi (py-0.19.16-py-1.0.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 457 | 0.2959 |
| tokenBased | 114 | 0.1575 |
| treeBased | 454 | 0.3040 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 457 | 457 | +0 | false |
| tokenBased | 3 | 114 | -111 | true |
| treeBased | 3 | 454 | -451 | true |

```json
{
  "total": 457,
  "replacement_api": "polars.expr.expr.Expr.replace",
  "threshold_10pct": 45.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 457,
      "score": 0.276425
    },
    "tokenBased": {
      "rank": 3,
      "score": 0.272251
    },
    "treeBased": {
      "rank": 3,
      "score": 0.302613
    }
  },
  "vi": {
    "mapBased": {
      "rank": 457,
      "score": 0.295947
    },
    "tokenBased": {
      "rank": 114,
      "score": 0.15748
    },
    "treeBased": {
      "rank": 454,
      "score": 0.303965
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 457,
      "vi_rank": 457,
      "delta": 0,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 3,
      "vi_rank": 114,
      "delta": -111,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 3,
      "vi_rank": 454,
      "delta": -451,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `polars.expr.expr.Expr.map_dict/Vi-1_py-0.19.15.py`
- **new**: `polars.expr.expr.Expr.map_dict/Vi_py-0.19.16.py`
- **+9 / -172**

```diff
--- polars.expr.expr.Expr.map_dict/Vi-1_py-0.19.15.py
+++ polars.expr.expr.Expr.map_dict/Vi_py-0.19.16.py
@@ -1,179 +1,16 @@
+    @deprecate_function(
+        "It has been renamed to `replace`."
+        " The default behavior has changed to keep any values not present in the mapping unchanged."
+        " Pass `default=None` to keep existing behavior.",
+        version="0.19.16",
+    )
+    @deprecate_renamed_parameter("remapping", "mapping", version="0.19.16")
     def map_dict(
         self,
-        remapping: dict[Any, Any],
+        mapping: dict[Any, Any],
         *,
         default: Any = None,
         return_dtype: PolarsDataType | None = None,
     ) -> Self:
         
-
-        def _remap_key_or_value_series(
-            name: str,
-            values: Iterable[Any],
-            dtype: PolarsDataType | None,
-            dtype_if_empty: PolarsDataType | None,
-            dtype_keys: PolarsDataType | None,
-            *,
-            is_keys: bool,
-        ) -> Series:
-            
-            try:
-                if dtype is None:
-
-
-
-                    s = pl.Series(
-                        name,
-                        values,
-                        dtype=None,
-                        dtype_if_empty=dtype_if_empty,
-                        strict=True,
-                    )
-
-                    if dtype_keys is not None:
-                        if s.dtype == dtype_keys:
-
-                            dtype = s.dtype
-                        elif (
-                            (s.dtype.is_integer() and dtype_keys.is_integer())
-                            or (s.dtype.is_float() and dtype_keys.is_float())
-                            or (s.dtype == Utf8 and dtype_keys == Categorical)
-                        ):
-
-
-
-                            dtype = dtype_keys
-                            s = pl.Series(
-                                name,
-                                values,
-                                dtype=dtype_keys,
-                                dtype_if_empty=dtype_if_empty,
-                                strict=True,
-                            )
-                            if dtype != s.dtype:
-                                raise ValueError(
-                                    f"remapping values for `map_dict` could not be converted to {dtype!r}: found {s.dtype!r}"
-                                )
-                else:
-
-
-
-
-                    s = pl.Series(
-                        name,
-                        values,
-                        dtype=dtype,
-                        dtype_if_empty=dtype_if_empty,
-                        strict=True,
-                    )
-                    if dtype != s.dtype:
-                        raise ValueError(
-                            f"remapping {'keys' if is_keys else 'values'} for `map_dict` could not be converted to {dtype!r}: found {s.dtype!r}"
-                        )
-
-            except OverflowError as exc:
-                if is_keys:
-                    raise ValueError(
-                        f"remapping keys for `map_dict` could not be converted to {dtype!r}: {exc!s}"
-                    ) from exc
-                else:
-                    raise ValueError(
-                        f"choose a more suitable output dtype for `map_dict` as remapping value could not be converted to {dtype!r}: {exc!s}"
-                    ) from exc
-
-            if is_keys:
-
-                if s.null_count() == 0:
-                    pass
-                elif s.null_count() == 1 and None in remapping:
-                    pass
-                else:
-                    raise ValueError(
-                        f"remapping keys for `map_dict` could not be converted to {dtype!r} without losing values in the conversion"
-                    )
-            else:
-
-                if s.null_count() == 0:
-                    pass
-                elif s.len() - s.null_count() == len(list(filter(None, values))):
-                    pass
-                else:
-                    raise ValueError(
-                        f"remapping values for `map_dict` could not be converted to {dtype!r} without losing values in the conversion"
-                    )
-            return s
-
-        def inner_func(s: Series, default_value: Any = None) -> Series:
-
-
-
-            df = s.to_frame().unnest(s.name) if s.dtype == Struct else s.to_frame()
-
-
-            column = df.columns[0]
-            input_dtype = df.dtypes[0]
-            remap_key_column = f"__POLARS_REMAP_KEY_{column}"
-            remap_value_column = f"__POLARS_REMAP_VALUE_{column}"
-            is_remapped_column = f"__POLARS_REMAP_IS_REMAPPED_{column}"
-
-
-
-
-
-            return_dtype_ = (
-                df.lazy().select(default).dtypes[0]
-                if return_dtype is None and isinstance(default, Expr)
-                else return_dtype
-            )
-            remap_key_s = _remap_key_or_value_series(
-                name=remap_key_column,
-                values=remapping.keys(),
-                dtype=input_dtype,
-                dtype_if_empty=input_dtype,
-                dtype_keys=input_dtype,
-                is_keys=True,
-            )
-            if return_dtype_:
-
-                remap_value_s = pl.Series(
-                    remap_value_column,
-                    remapping.values(),
-                    dtype=return_dtype_,
-                    dtype_if_empty=input_dtype,
-                )
-            else:
-
-
-
-                remap_value_s = _remap_key_or_value_series(
-                    name=remap_value_column,
-                    values=remapping.values(),
-                    dtype=None,
-                    dtype_if_empty=input_dtype,
-                    dtype_keys=input_dtype,
-                    is_keys=False,
-                )
-
-            remap_frame = pl.LazyFrame(data=[remap_key_s, remap_value_s]).with_columns(
-                F.lit(True).alias(is_remapped_column)
-            )
-            mapped = df.lazy().join(
-                other=remap_frame, how="left", left_on=column, right_on=remap_key_column
-            )
-            if default_value is None:
-                result_index = 1
-            else:
-                expr_default = parse_as_expression(default_value, str_as_lit=True)
-                default_parsed = self._from_pyexpr(expr_default)
-                mapped = mapped.select(
-                    F.when(F.col(is_remapped_column).is_not_null())
-                    .then(F.col(remap_value_column))
-                    .otherwise(default_parsed)
-                    .alias(column)
-                )
-                result_index = 0
-
-            return mapped.collect(no_optimization=True).to_series(index=result_index)
-
-        remapping_func = partial(inner_func, default_value=default)
-        return self.map_batches(function=remapping_func, return_dtype=return_dtype)
+        return self.replace(mapping, default=default, return_dtype=return_dtype)
```

```json
{
  "old_file": "polars.expr.expr.Expr.map_dict/Vi-1_py-0.19.15.py",
  "new_file": "polars.expr.expr.Expr.map_dict/Vi_py-0.19.16.py",
  "lines_added": 9,
  "lines_removed": 172
}
```
