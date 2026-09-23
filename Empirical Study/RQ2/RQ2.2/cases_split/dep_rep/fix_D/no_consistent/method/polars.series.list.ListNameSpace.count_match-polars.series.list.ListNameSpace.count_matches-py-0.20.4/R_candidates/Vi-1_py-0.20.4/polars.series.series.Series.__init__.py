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
        # If 'Unknown' treat as None to attempt inference
        if dtype == Unknown:
            dtype = None

        # Raise early error on invalid dtype
        if (
            dtype is not None
            and not is_polars_dtype(dtype)
            and py_type_to_dtype(dtype, raise_unmatched=False) is None
        ):
            msg = f"given dtype: {dtype!r} is not a valid Polars data type and cannot be converted into one"
            raise ValueError(msg)

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

        if values is None:
            self._s = sequence_to_pyseries(
                name, [], dtype=dtype, dtype_if_empty=dtype_if_empty
            )

        elif isinstance(values, range):
            self._s = range_to_series(name, values, dtype=dtype)._s

        elif isinstance(values, Series):
            name = values.name if original_name is None else name
            self._s = series_to_pyseries(name, values, dtype=dtype, strict=strict)

        elif isinstance(values, Sequence):
            self._s = sequence_to_pyseries(
                name,
                values,
                dtype=dtype,
                strict=strict,
                dtype_if_empty=dtype_if_empty,
                nan_to_null=nan_to_null,
            )

        elif _check_for_numpy(values) and isinstance(values, np.ndarray):
            self._s = numpy_to_pyseries(
                name, values, strict=strict, nan_to_null=nan_to_null
            )
            if values.dtype.type in [np.datetime64, np.timedelta64]:
                # cast to appropriate dtype, handling NaT values
                dtype = _resolve_temporal_dtype(dtype, values.dtype)
                if dtype is not None:
                    self._s = (
                        self.cast(dtype)
                        .scatter(np.argwhere(np.isnat(values)).flatten(), None)
                        ._s
                    )
                    return

            if dtype is not None:
                self._s = self.cast(dtype, strict=True)._s

        elif _check_for_pyarrow(values) and isinstance(
            values, (pa.Array, pa.ChunkedArray)
        ):
            self._s = arrow_to_pyseries(name, values)

        elif _check_for_pandas(values) and isinstance(
            values, (pd.Series, pd.DatetimeIndex)
        ):
            self._s = pandas_to_pyseries(name, values)

        elif _is_generator(values):
            self._s = iterable_to_pyseries(
                name,
                values,
                dtype=dtype,
                dtype_if_empty=dtype_if_empty,
                strict=strict,
            )

        elif isinstance(values, pl.DataFrame):
            to_struct = values.width > 1
            name = (
                values.columns[0] if (original_name is None and not to_struct) else name
            )
            s = values.to_struct(name) if to_struct else values.to_series().rename(name)
            if dtype is not None and dtype != s.dtype:
                s = s.cast(dtype)
            self._s = s._s

        else:
            msg = (
                f"Series constructor called with unsupported type {type(values).__name__!r}"
                " for the `values` parameter"
            )
            raise TypeError(msg)
