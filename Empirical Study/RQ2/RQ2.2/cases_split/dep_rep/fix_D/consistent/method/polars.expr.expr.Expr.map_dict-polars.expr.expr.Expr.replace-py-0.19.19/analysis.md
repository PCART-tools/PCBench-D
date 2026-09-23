# 一、突变情况分析

- **Total**: 443
- **替代API**: `polars.expr.expr.Expr.replace`
- **10% 阈值**: 44.3

## Vi-1 (py-0.19.15-py-0.19.19)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 44 | 0.7504 |
| tokenBased | 1 | 0.9583 |
| treeBased | 1 | 0.9881 |

## Vi (py-0.19.15-py-0.20.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 436 | 0.3885 |
| tokenBased | 2 | 0.2447 |
| treeBased | 2 | 0.2641 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 44 | 436 | -392 | true |
| tokenBased | 1 | 2 | -1 | false |
| treeBased | 1 | 2 | -1 | false |

```json
{
  "total": 443,
  "replacement_api": "polars.expr.expr.Expr.replace",
  "threshold_10pct": 44.3,
  "vi_minus_1": {
    "mapBased": {
      "rank": 44,
      "score": 0.750442
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.95825
    },
    "treeBased": {
      "rank": 1,
      "score": 0.988149
    }
  },
  "vi": {
    "mapBased": {
      "rank": 436,
      "score": 0.388459
    },
    "tokenBased": {
      "rank": 2,
      "score": 0.244681
    },
    "treeBased": {
      "rank": 2,
      "score": 0.264069
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 44,
      "vi_rank": 436,
      "delta": -392,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 1,
      "vi_rank": 2,
      "delta": -1,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `R_candidates/Vi-1_py-0.19.19/polars.expr.expr.Expr.replace.py`
- **new**: `R_candidates/Vi_py-0.20.0/polars.expr.expr.Expr.replace.py`
- **+19 / -173**

```diff
--- R_candidates/Vi-1_py-0.19.19/polars.expr.expr.Expr.replace.py
+++ R_candidates/Vi_py-0.20.0/polars.expr.expr.Expr.replace.py
@@ -1,182 +1,28 @@
     def replace(
         self,
-        mapping: dict[Any, Any],
+        old: IntoExpr | Sequence[Any] | Mapping[Any, Any],
+        new: IntoExpr | Sequence[Any] | NoDefault = no_default,
         *,
-        default: Any = no_default,
+        default: IntoExpr | NoDefault = no_default,
         return_dtype: PolarsDataType | None = None,
     ) -> Self:
         
+        if new is no_default and isinstance(old, Mapping):
+            new = pl.Series(old.values())
+            old = pl.Series(old.keys())
+        else:
+            if isinstance(old, Sequence) and not isinstance(old, (str, pl.Series)):
+                old = pl.Series(old)
+            if isinstance(new, Sequence) and not isinstance(new, (str, pl.Series)):
+                new = pl.Series(new)
 
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
+        old = parse_as_expression(old, str_as_lit=True)
+        new = parse_as_expression(new, str_as_lit=True)
 
+        default = (
+            None
+            if default is no_default
+            else parse_as_expression(default, str_as_lit=True)
+        )
 
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
-                                    f"mapping values for `replace` could not be converted to {dtype!r}: found {s.dtype!r}"
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
-                            f"mapping {'keys' if is_keys else 'values'} for `replace` could not be converted to {dtype!r}: found {s.dtype!r}"
-                        )
-
-            except OverflowError as exc:
-                if is_keys:
-                    raise ValueError(
-                        f"mapping keys for `replace` could not be converted to {dtype!r}: {exc!s}"
-                    ) from exc
-                else:
-                    raise ValueError(
-                        f"choose a more suitable output dtype for `replace` as mapping value could not be converted to {dtype!r}: {exc!s}"
-                    ) from exc
-
-            if is_keys:
-
-                if s.null_count() == 0:
-                    pass
-                elif s.null_count() == 1 and None in mapping:
-                    pass
-                else:
-                    raise ValueError(
-                        f"mapping keys for `replace` could not be converted to {dtype!r} without losing values in the conversion"
-                    )
-            else:
-
-                if s.null_count() == 0:
-                    pass
-                elif s.len() - s.null_count() == len(list(filter(None, values))):
-                    pass
-                else:
-                    raise ValueError(
-                        f"remapping values for `replace` could not be converted to {dtype!r} without losing values in the conversion"
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
-                values=mapping.keys(),
-                dtype=input_dtype,
-                dtype_if_empty=input_dtype,
-                dtype_keys=input_dtype,
-                is_keys=True,
-            )
-            if return_dtype_:
-
-                remap_value_s = pl.Series(
-                    remap_value_column,
-                    mapping.values(),
-                    dtype=return_dtype_,
-                    dtype_if_empty=input_dtype,
-                )
-            else:
-
-
-
-                remap_value_s = _remap_key_or_value_series(
-                    name=remap_value_column,
-                    values=mapping.values(),
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
-        if default is no_default:
-            default = F.first()
-
-        mapping_func = partial(inner_func, default_value=default)
-        return self.map_batches(function=mapping_func, return_dtype=return_dtype)
+        return self._from_pyexpr(self._pyexpr.replace(old, new, default, return_dtype))
```

```json
{
  "old_file": "R_candidates/Vi-1_py-0.19.19/polars.expr.expr.Expr.replace.py",
  "new_file": "R_candidates/Vi_py-0.20.0/polars.expr.expr.Expr.replace.py",
  "lines_added": 19,
  "lines_removed": 173
}
```
