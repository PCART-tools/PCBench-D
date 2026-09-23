    def __init__(
        self,
        name: str | ArrayLike | None = None,
        values: ArrayLike | None = None,
        dtype: PolarsDataType | None = None,
        *,
        strict: bool = True,
        nan_to_null: bool = False,
        dtype_if_empty: PolarsDataType = Null,
    ):
        if dtype_if_empty != Null:
            issue_deprecation_warning(
                "The `dtype_if_empty` parameter for the Series constructor is deprecated."
                " The data type for empty Series will always be Null, unless `dtype` is specified."
                " To preserve behavior, check if the resulting Series has data type Null and cast to the desired data type."
                " This parameter will be removed in the next breaking release.",
                version="0.20.6",
            )

        # If 'Unknown' treat as None to trigger type inference
        if dtype == Unknown:
            dtype = None
        elif dtype is not None and not is_polars_dtype(dtype):
            # Raise early error on invalid dtype
            if not is_polars_dtype(
                pl_dtype := py_type_to_dtype(dtype, raise_unmatched=False)
            ):
                msg = f"given dtype: {dtype!r} is not a valid Polars data type and cannot be converted into one"
                raise ValueError(msg)
            else:
                dtype = pl_dtype

        # Handle case where values are passed as the first argument
        original_name: str | None = None
        if name is None:
            name = ""
        elif isinstance(name, str):
            original_name = name
        else:
            if values is None:
                values = name
                name = ""
            else:
                msg = "Series name must be a string"
                raise TypeError(msg)

        if isinstance(values, Sequence):
            self._s = sequence_to_pyseries(
                name,
                values,
                dtype=dtype,
                strict=strict,
                nan_to_null=nan_to_null,
            )

        elif values is None:
            self._s = sequence_to_pyseries(name, [], dtype=dtype)

        elif _check_for_numpy(values) and isinstance(values, np.ndarray):
            self._s = numpy_to_pyseries(
                name, values, strict=strict, nan_to_null=nan_to_null
            )
            if values.dtype.type in [np.datetime64, np.timedelta64]:
                # cast to appropriate dtype, handling NaT values
                input_dtype = _resolve_temporal_dtype(None, values.dtype)
                dtype = _resolve_temporal_dtype(dtype, values.dtype)
                if dtype is not None:
                    self._s = (
                        # `values.dtype` has already been validated in
                        # `numpy_to_pyseries`, so `input_dtype` can't be `None`
                        self.cast(input_dtype, strict=False)  # type: ignore[arg-type]
                        .cast(dtype)
                        .scatter(np.argwhere(np.isnat(values)).flatten(), None)
                        ._s
                    )
                    return

            if dtype is not None:
                self._s = self.cast(dtype, strict=strict)._s

        elif _check_for_pyarrow(values) and isinstance(
            values, (pa.Array, pa.ChunkedArray)
        ):
            self._s = arrow_to_pyseries(name, values, dtype=dtype, strict=strict)

        elif _check_for_pandas(values) and isinstance(
            values, (pd.Series, pd.Index, pd.DatetimeIndex)
        ):
            self._s = pandas_to_pyseries(name, values, dtype=dtype, strict=strict)

        elif _is_generator(values):
            self._s = iterable_to_pyseries(name, values, dtype=dtype, strict=strict)

        elif isinstance(values, Series):
            self._s = series_to_pyseries(
                original_name, values, dtype=dtype, strict=strict
            )

        elif isinstance(values, pl.DataFrame):
            self._s = dataframe_to_pyseries(
                original_name, values, dtype=dtype, strict=strict
            )

        else:
            msg = (
                f"Series constructor called with unsupported type {type(values).__name__!r}"
                " for the `values` parameter"
            )
            raise TypeError(msg)

        # Implementation of deprecated `dtype_if_empty` functionality
        if dtype_if_empty != Null and self.dtype == Null:
            self._s = self._s.cast(dtype_if_empty, False)
