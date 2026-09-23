    def map_dict(
        self,
        remapping: dict[Any, Any],
        *,
        default: Any = None,
        return_dtype: PolarsDataType | None = None,
    ) -> Self:
        """
        Replace values in column according to remapping dictionary.

        Needs a global string cache for lazily evaluated queries on columns of
        type ``pl.Categorical``.

        Parameters
        ----------
        remapping
            Dictionary containing the before/after values to map.
        default
            Value to use when the remapping dict does not contain the lookup value.
            Accepts expression input. Non-expression inputs are parsed as literals.
            Use ``pl.first()``, to keep the original value.
        return_dtype
            Set return dtype to override automatic return dtype determination.

        See Also
        --------
        map

        Examples
        --------
        >>> country_code_dict = {
        ...     "CA": "Canada",
        ...     "DE": "Germany",
        ...     "FR": "France",
        ...     None: "Not specified",
        ... }
        >>> df = pl.DataFrame(
        ...     {
        ...         "country_code": ["FR", None, "ES", "DE"],
        ...     }
        ... ).with_row_count()
        >>> df
        shape: (4, 2)
        ┌────────┬──────────────┐
        │ row_nr ┆ country_code │
        │ ---    ┆ ---          │
        │ u32    ┆ str          │
        ╞════════╪══════════════╡
        │ 0      ┆ FR           │
        │ 1      ┆ null         │
        │ 2      ┆ ES           │
        │ 3      ┆ DE           │
        └────────┴──────────────┘

        >>> df.with_columns(
        ...     pl.col("country_code").map_dict(country_code_dict).alias("remapped")
        ... )
        shape: (4, 3)
        ┌────────┬──────────────┬───────────────┐
        │ row_nr ┆ country_code ┆ remapped      │
        │ ---    ┆ ---          ┆ ---           │
        │ u32    ┆ str          ┆ str           │
        ╞════════╪══════════════╪═══════════════╡
        │ 0      ┆ FR           ┆ France        │
        │ 1      ┆ null         ┆ Not specified │
        │ 2      ┆ ES           ┆ null          │
        │ 3      ┆ DE           ┆ Germany       │
        └────────┴──────────────┴───────────────┘

        Set a default value for values that cannot be mapped...

        >>> df.with_columns(
        ...     pl.col("country_code")
        ...     .map_dict(country_code_dict, default="unknown")
        ...     .alias("remapped")
        ... )
        shape: (4, 3)
        ┌────────┬──────────────┬───────────────┐
        │ row_nr ┆ country_code ┆ remapped      │
        │ ---    ┆ ---          ┆ ---           │
        │ u32    ┆ str          ┆ str           │
        ╞════════╪══════════════╪═══════════════╡
        │ 0      ┆ FR           ┆ France        │
        │ 1      ┆ null         ┆ Not specified │
        │ 2      ┆ ES           ┆ unknown       │
        │ 3      ┆ DE           ┆ Germany       │
        └────────┴──────────────┴───────────────┘

        ...or keep the original value, by making use of ``pl.first()``:

        >>> df.with_columns(
        ...     pl.col("country_code")
        ...     .map_dict(country_code_dict, default=pl.first())
        ...     .alias("remapped")
        ... )
        shape: (4, 3)
        ┌────────┬──────────────┬───────────────┐
        │ row_nr ┆ country_code ┆ remapped      │
        │ ---    ┆ ---          ┆ ---           │
        │ u32    ┆ str          ┆ str           │
        ╞════════╪══════════════╪═══════════════╡
        │ 0      ┆ FR           ┆ France        │
        │ 1      ┆ null         ┆ Not specified │
        │ 2      ┆ ES           ┆ ES            │
        │ 3      ┆ DE           ┆ Germany       │
        └────────┴──────────────┴───────────────┘

        ...or keep the original value, by explicitly referring to the column:

        >>> df.with_columns(
        ...     pl.col("country_code")
        ...     .map_dict(country_code_dict, default=pl.col("country_code"))
        ...     .alias("remapped")
        ... )
        shape: (4, 3)
        ┌────────┬──────────────┬───────────────┐
        │ row_nr ┆ country_code ┆ remapped      │
        │ ---    ┆ ---          ┆ ---           │
        │ u32    ┆ str          ┆ str           │
        ╞════════╪══════════════╪═══════════════╡
        │ 0      ┆ FR           ┆ France        │
        │ 1      ┆ null         ┆ Not specified │
        │ 2      ┆ ES           ┆ ES            │
        │ 3      ┆ DE           ┆ Germany       │
        └────────┴──────────────┴───────────────┘

        If you need to access different columns to set a default value, a struct needs
        to be constructed; in the first field is the column that you want to remap and
        the rest of the fields are the other columns used in the default expression.

        >>> df.with_columns(
        ...     pl.struct(pl.col(["country_code", "row_nr"])).map_dict(
        ...         remapping=country_code_dict,
        ...         default=pl.col("row_nr").cast(pl.Utf8),
        ...     )
        ... )
        shape: (4, 2)
        ┌────────┬───────────────┐
        │ row_nr ┆ country_code  │
        │ ---    ┆ ---           │
        │ u32    ┆ str           │
        ╞════════╪═══════════════╡
        │ 0      ┆ France        │
        │ 1      ┆ Not specified │
        │ 2      ┆ 2             │
        │ 3      ┆ Germany       │
        └────────┴───────────────┘

        Override return dtype:

        >>> df.with_columns(
        ...     pl.col("row_nr")
        ...     .map_dict({1: 7, 3: 4}, default=3, return_dtype=pl.UInt8)
        ...     .alias("remapped")
        ... )
        shape: (4, 3)
        ┌────────┬──────────────┬──────────┐
        │ row_nr ┆ country_code ┆ remapped │
        │ ---    ┆ ---          ┆ ---      │
        │ u32    ┆ str          ┆ u8       │
        ╞════════╪══════════════╪══════════╡
        │ 0      ┆ FR           ┆ 3        │
        │ 1      ┆ null         ┆ 7        │
        │ 2      ┆ ES           ┆ 3        │
        │ 3      ┆ DE           ┆ 4        │
        └────────┴──────────────┴──────────┘

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
            Convert remapping keys or remapping values to `Series` with `dtype`.

            Try to convert the remapping keys or remapping values to `Series` with
            the specified dtype and check that none of the values are accidentally
            lost (replaced by nulls) during the conversion.

            Parameters
            ----------
            name
                Name of the keys or values series.
            values
                Values for the series: `remapping.keys()` or `remapping.values()`.
            dtype
                User specified dtype. If None,
            dtype_if_empty
                If no dtype is specified and values contains None, an empty list,
                or a list with only None values, set the Polars dtype of the Series
                data.
            dtype_keys
                If user set dtype is None, try to see if Series for remapping.values()
                can be converted to same dtype as the remapping.keys() Series dtype.
            is_keys
                If values contains keys or values from remapping dict.

            """
            try:
                if dtype is None:
                    # If no dtype was set, which should only happen when:
                    #     values = remapping.values()
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
                            (s.dtype in INTEGER_DTYPES and dtype_keys in INTEGER_DTYPES)
                            or (s.dtype in FLOAT_DTYPES and dtype_keys in FLOAT_DTYPES)
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
                                    f"remapping values for `map_dict` could not be converted to {dtype!r}: found {s.dtype!r}"
                                )
                else:
                    # dtype was set, which should always be the case when:
                    #     values = remapping.keys()
                    # and in cases where the user set the output dtype when:
                    #     values = remapping.values()
                    s = pl.Series(
                        name,
                        values,
                        dtype=dtype,
                        dtype_if_empty=dtype_if_empty,
                        strict=True,
                    )
                    if dtype != s.dtype:
                        raise ValueError(
                            f"remapping {'keys' if is_keys else 'values'} for `map_dict` could not be converted to {dtype!r}: found {s.dtype!r}"
                        )

            except OverflowError as exc:
                if is_keys:
                    raise ValueError(
                        f"remapping keys for `map_dict` could not be converted to {dtype!r}: {exc!s}"
                    ) from exc
                else:
                    raise ValueError(
                        f"choose a more suitable output dtype for map_dict as remapping value could not be converted to {dtype!r}: {exc!s}"
                    ) from exc

            if is_keys:
                # values = remapping.keys()
                if s.null_count() == 0:  # noqa: SIM114
                    pass
                elif s.null_count() == 1 and None in remapping:
                    pass
                else:
                    raise ValueError(
                        f"remapping keys for `map_dict` could not be converted to {dtype!r} without losing values in the conversion"
                    )
            else:
                # values = remapping.values()
                if s.null_count() == 0:  # noqa: SIM114
                    pass
                elif s.len() - s.null_count() == len(list(filter(None, values))):
                    pass
                else:
                    raise ValueError(
                        f"remapping values for `map_dict` could not be converted to {dtype!r} without losing values in the conversion"
                    )

            return s

        # Use two functions to save unneeded work.
        # This factors out allocations and branches.
        def inner_with_default(s: Series) -> Series:
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
                values=remapping.keys(),
                dtype=input_dtype,
                dtype_if_empty=input_dtype,
                dtype_keys=input_dtype,
                is_keys=True,
            )

            if return_dtype_:
                # Create remap value Series with specified output dtype.
                remap_value_s = pl.Series(
                    remap_value_column,
                    remapping.values(),
                    dtype=return_dtype_,
                    dtype_if_empty=input_dtype,
                )
            else:
                # Create remap value Series with same output dtype as remap key Series,
                # if possible (if both are integers, both are floats or remap value
                # Series is pl.Utf8 and remap key Series is pl.Categorical).
                remap_value_s = _remap_key_or_value_series(
                    name=remap_value_column,
                    values=remapping.values(),
                    dtype=None,
                    dtype_if_empty=input_dtype,
                    dtype_keys=input_dtype,
                    is_keys=False,
                )

            default_parsed = self._from_pyexpr(
                parse_as_expression(default, str_as_lit=True)
            )
            return (
                (
                    df.lazy()
                    .join(
                        pl.DataFrame(
                            [
                                remap_key_s,
                                remap_value_s,
                            ]
                        )
                        .lazy()
                        .with_columns(F.lit(True).alias(is_remapped_column)),
                        how="left",
                        left_on=column,
                        right_on=remap_key_column,
                    )
                    .select(
                        F.when(F.col(is_remapped_column).is_not_null())
                        .then(F.col(remap_value_column))
                        .otherwise(default_parsed)
                        .alias(column)
                    )
                )
                .collect(no_optimization=True)
                .to_series()
            )

        def inner(s: Series) -> Series:
            column = s.name
            input_dtype = s.dtype
            remap_key_column = f"__POLARS_REMAP_KEY_{column}"
            remap_value_column = f"__POLARS_REMAP_VALUE_{column}"
            is_remapped_column = f"__POLARS_REMAP_IS_REMAPPED_{column}"

            remap_key_s = _remap_key_or_value_series(
                name=remap_key_column,
                values=list(remapping.keys()),
                dtype=input_dtype,
                dtype_if_empty=input_dtype,
                dtype_keys=input_dtype,
                is_keys=True,
            )

            if return_dtype:
                # Create remap value Series with specified output dtype.
                remap_value_s = pl.Series(
                    remap_value_column,
                    remapping.values(),
                    dtype=return_dtype,
                    dtype_if_empty=input_dtype,
                )
            else:
                # Create remap value Series with same output dtype as remap key Series,
                # if possible (if both are integers, both are floats or remap value
                # Series is pl.Utf8 and remap key Series is pl.Categorical).
                remap_value_s = _remap_key_or_value_series(
                    name=remap_value_column,
                    values=remapping.values(),
                    dtype=None,
                    dtype_if_empty=input_dtype,
                    dtype_keys=input_dtype,
                    is_keys=False,
                )

            return (
                (
                    s.to_frame()
                    .lazy()
                    .join(
                        pl.DataFrame(
                            [
                                remap_key_s,
                                remap_value_s,
                            ]
                        )
                        .lazy()
                        .with_columns(F.lit(True).alias(is_remapped_column)),
                        how="left",
                        left_on=column,
                        right_on=remap_key_column,
                    )
                )
                .collect(no_optimization=True)
                .to_series(1)
            )

        func = inner_with_default if default is not None else inner
        return self.map_batches(func)
