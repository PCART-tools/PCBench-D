    def replace(
        self,
        mapping: dict[Any, Any],
        *,
        default: Any = no_default,
        return_dtype: PolarsDataType | None = None,
    ) -> Self:
        """
        Replace values according to the given mapping.

        Needs a global string cache for lazily evaluated queries on columns of
        type `Categorical`.

        Parameters
        ----------
        mapping
            Mapping of values to their replacement.
        default
            Value to use when the mapping does not contain the lookup value.
            Defaults to keeping the original value. Accepts expression input.
            Non-expression inputs are parsed as literals.
        return_dtype
            Set return dtype to override automatic return dtype determination.

        See Also
        --------
        str.replace

        Examples
        --------
        Replace a single value by another value. Values not in the mapping remain
        unchanged.

        >>> df = pl.DataFrame({"a": [1, 2, 2, 3]})
        >>> df.with_columns(pl.col("a").replace({2: 100}).alias("replaced"))
        shape: (4, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ i64 ┆ i64      │
        ╞═════╪══════════╡
        │ 1   ┆ 1        │
        │ 2   ┆ 100      │
        │ 2   ┆ 100      │
        │ 3   ┆ 3        │
        └─────┴──────────┘

        Replace multiple values. Specify a default to set values not in the given map
        to the default value.

        >>> df = pl.DataFrame({"country_code": ["FR", "ES", "DE", None]})
        >>> country_code_map = {
        ...     "CA": "Canada",
        ...     "DE": "Germany",
        ...     "FR": "France",
        ...     None: "unspecified",
        ... }
        >>> df.with_columns(
        ...     pl.col("country_code")
        ...     .replace(country_code_map, default=None)
        ...     .alias("replaced")
        ... )
        shape: (4, 2)
        ┌──────────────┬─────────────┐
        │ country_code ┆ replaced    │
        │ ---          ┆ ---         │
        │ str          ┆ str         │
        ╞══════════════╪═════════════╡
        │ FR           ┆ France      │
        │ ES           ┆ null        │
        │ DE           ┆ Germany     │
        │ null         ┆ unspecified │
        └──────────────┴─────────────┘

        The return type can be overridden with the `return_dtype` argument.

        >>> df = df.with_row_count()
        >>> df.select(
        ...     "row_nr",
        ...     pl.col("row_nr")
        ...     .replace({1: 10, 2: 20}, default=0, return_dtype=pl.UInt8)
        ...     .alias("replaced"),
        ... )
        shape: (4, 2)
        ┌────────┬──────────┐
        │ row_nr ┆ replaced │
        │ ---    ┆ ---      │
        │ u32    ┆ u8       │
        ╞════════╪══════════╡
        │ 0      ┆ 0        │
        │ 1      ┆ 10       │
        │ 2      ┆ 20       │
        │ 3      ┆ 0        │
        └────────┴──────────┘

        To reference other columns as a `default` value, a struct column must be
        constructed first. The first field must be the column in which values are
        replaced. The other columns can be used in the default expression.

        >>> df.with_columns(
        ...     pl.struct("country_code", "row_nr")
        ...     .replace(
        ...         mapping=country_code_map,
        ...         default=pl.col("row_nr").cast(pl.Utf8),
        ...     )
        ...     .alias("replaced")
        ... )
        shape: (4, 3)
        ┌────────┬──────────────┬─────────────┐
        │ row_nr ┆ country_code ┆ replaced    │
        │ ---    ┆ ---          ┆ ---         │
        │ u32    ┆ str          ┆ str         │
        ╞════════╪══════════════╪═════════════╡
        │ 0      ┆ FR           ┆ France      │
        │ 1      ┆ ES           ┆ 1           │
        │ 2      ┆ DE           ┆ Germany     │
        │ 3      ┆ null         ┆ unspecified │
        └────────┴──────────────┴─────────────┘
        """

        def _remap_key_or_value_series(
            name: str,
            values: Iterable[Any],
            dtype: PolarsDataType | None,
            dtype_if_empty: PolarsDataType | None,
            dtype_keys: PolarsDataType | None,
            *,
            is_keys: bool,
        ) -> Series:
            """
            Convert mapping keys or mapping values to `Series` with `dtype`.

            Try to convert the mapping keys or mapping values to `Series` with
            the specified dtype and check that none of the values are accidentally
            lost (replaced by nulls) during the conversion.

            Parameters
            ----------
            name
                Name of the keys or values Series.
            values
                Values for the Series: `mapping.keys()` or `mapping.values()`.
            dtype
                User specified dtype. If None,
            dtype_if_empty
                If no dtype is specified and values contains None, an empty list,
                or a list with only None values, set the Polars dtype of the Series
                data.
            dtype_keys
                If user set dtype is None, try to see if Series for mapping.values()
                can be converted to same dtype as the mapping.keys() Series dtype.
            is_keys
                If values contains keys or values from mapping dict.

            """
            try:
                if dtype is None:
                    # If no dtype was set, which should only happen when:
                    #     values = mapping.values()
                    # create a Series from those values and infer the dtype.
                    s = pl.Series(
                        name,
                        values,
                        dtype=None,
                        dtype_if_empty=dtype_if_empty,
                        strict=True,
                    )

                    if dtype_keys is not None:
                        if s.dtype == dtype_keys:
                            # Values Series has same dtype as keys Series.
                            dtype = s.dtype
                        elif (
                            (s.dtype.is_integer() and dtype_keys.is_integer())
                            or (s.dtype.is_float() and dtype_keys.is_float())
                            or (s.dtype == Utf8 and dtype_keys == Categorical)
                        ):
                            # Values Series and keys Series are of similar dtypes,
                            # that we can assume that the user wants the values Series
                            # of the same dtype as the key Series.
                            dtype = dtype_keys
                            s = pl.Series(
                                name,
                                values,
                                dtype=dtype_keys,
                                dtype_if_empty=dtype_if_empty,
                                strict=True,
                            )
                            if dtype != s.dtype:
                                raise ValueError(
                                    f"mapping values for `replace` could not be converted to {dtype!r}: found {s.dtype!r}"
                                )
                else:
                    # dtype was set, which should always be the case when:
                    #     values = mapping.keys()
                    # and in cases where the user set the output dtype when:
                    #     values = mapping.values()
                    s = pl.Series(
                        name,
                        values,
                        dtype=dtype,
                        dtype_if_empty=dtype_if_empty,
                        strict=True,
                    )
                    if dtype != s.dtype:
                        raise ValueError(
                            f"mapping {'keys' if is_keys else 'values'} for `replace` could not be converted to {dtype!r}: found {s.dtype!r}"
                        )

            except OverflowError as exc:
                if is_keys:
                    raise ValueError(
                        f"mapping keys for `replace` could not be converted to {dtype!r}: {exc!s}"
                    ) from exc
                else:
                    raise ValueError(
                        f"choose a more suitable output dtype for `replace` as mapping value could not be converted to {dtype!r}: {exc!s}"
                    ) from exc

            if is_keys:
                # values = mapping.keys()
                if s.null_count() == 0:  # noqa: SIM114
                    pass
                elif s.null_count() == 1 and None in mapping:
                    pass
                else:
                    raise ValueError(
                        f"mapping keys for `replace` could not be converted to {dtype!r} without losing values in the conversion"
                    )
            else:
                # values = mapping.values()
                if s.null_count() == 0:  # noqa: SIM114
                    pass
                elif s.len() - s.null_count() == len(list(filter(None, values))):
                    pass
                else:
                    raise ValueError(
                        f"remapping values for `replace` could not be converted to {dtype!r} without losing values in the conversion"
                    )
            return s

        def inner_func(s: Series, default_value: Any = None) -> Series:
            # Convert Series to:
            #   - multicolumn DataFrame, if Series is a Struct.
            #   - one column DataFrame in other cases.
            df = s.to_frame().unnest(s.name) if s.dtype == Struct else s.to_frame()

            # For struct we always apply mapping to the first column.
            column = df.columns[0]
            input_dtype = df.dtypes[0]
            remap_key_column = f"__POLARS_REMAP_KEY_{column}"
            remap_value_column = f"__POLARS_REMAP_VALUE_{column}"
            is_remapped_column = f"__POLARS_REMAP_IS_REMAPPED_{column}"

            # Set output dtype:
            #  - to dtype, if specified.
            #  - to same dtype as expression specified as default value.
            #  - to None, if dtype was not specified and default was not an expression.
            return_dtype_ = (
                df.lazy().select(default).dtypes[0]
                if return_dtype is None and isinstance(default, Expr)
                else return_dtype
            )
            remap_key_s = _remap_key_or_value_series(
                name=remap_key_column,
                values=mapping.keys(),
                dtype=input_dtype,
                dtype_if_empty=input_dtype,
                dtype_keys=input_dtype,
                is_keys=True,
            )
            if return_dtype_:
                # Create remap value Series with specified output dtype.
                remap_value_s = pl.Series(
                    remap_value_column,
                    mapping.values(),
                    dtype=return_dtype_,
                    dtype_if_empty=input_dtype,
                )
            else:
                # Create remap value Series with same output dtype as remap key Series,
                # if possible (if both are integers, both are floats or remap value
                # Series is pl.Utf8 and remap key Series is pl.Categorical).
                remap_value_s = _remap_key_or_value_series(
                    name=remap_value_column,
                    values=mapping.values(),
                    dtype=None,
                    dtype_if_empty=input_dtype,
                    dtype_keys=input_dtype,
                    is_keys=False,
                )

            remap_frame = pl.LazyFrame(data=[remap_key_s, remap_value_s]).with_columns(
                F.lit(True).alias(is_remapped_column)
            )
            mapped = df.lazy().join(
                other=remap_frame, how="left", left_on=column, right_on=remap_key_column
            )
            if default_value is None:
                result_index = 1
            else:
                expr_default = parse_as_expression(default_value, str_as_lit=True)
                default_parsed = self._from_pyexpr(expr_default)
                mapped = mapped.select(
                    F.when(F.col(is_remapped_column).is_not_null())
                    .then(F.col(remap_value_column))
                    .otherwise(default_parsed)
                    .alias(column)
                )
                result_index = 0

            return mapped.collect(no_optimization=True).to_series(index=result_index)

        if default is no_default:
            default = F.first()

        mapping_func = partial(inner_func, default_value=default)
        return self.map_batches(function=mapping_func, return_dtype=return_dtype)
