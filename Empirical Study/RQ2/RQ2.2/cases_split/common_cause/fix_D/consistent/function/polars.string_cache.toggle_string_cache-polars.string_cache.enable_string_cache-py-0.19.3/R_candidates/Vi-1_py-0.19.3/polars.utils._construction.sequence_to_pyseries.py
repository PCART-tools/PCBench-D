def sequence_to_pyseries(
    name: str,
    values: Sequence[Any],
    dtype: PolarsDataType | None = None,
    *,
    dtype_if_empty: PolarsDataType | None = None,
    strict: bool = True,
    nan_to_null: bool = False,
) -> PySeries:
    """Construct a PySeries from a sequence."""
    python_dtype: type | None = None

    # empty sequence
    if not values and dtype is None:
        # if dtype for empty sequence could be guessed
        # (e.g comparisons between self and other), default to Float32
        dtype = dtype_if_empty or Float32

    # lists defer to subsequent handling; identify nested type
    elif dtype == List:
        getattr(dtype, "inner", None)
        python_dtype = list

    # infer temporal type handling
    py_temporal_types = {date, datetime, timedelta, time}
    pl_temporal_types = {Date, Datetime, Duration, Time}

    value = _get_first_non_none(values)
    if value is not None:
        if (
            dataclasses.is_dataclass(value)
            or is_pydantic_model(value)
            or is_namedtuple(value.__class__, annotated=True)
        ):
            return pl.DataFrame(values).to_struct(name)._s
        elif isinstance(value, range):
            values = [range_to_series("", v) for v in values]
        else:
            # for temporal dtypes:
            # * if the values are integer, we take the physical branch.
            # * if the values are python types, take the temporal branch.
            # * if the values are ISO-8601 strings, init then convert via strptime.
            # * if the values are floats/other dtypes, this is an error.
            if dtype in py_temporal_types and isinstance(value, int):
                dtype = py_type_to_dtype(dtype)  # construct from integer
            elif (
                dtype in pl_temporal_types or type(dtype) in pl_temporal_types
            ) and not isinstance(value, int):
                python_dtype = dtype_to_py_type(dtype)  # type: ignore[arg-type]

    # physical branch
    # flat data
    if (
        dtype is not None
        and dtype not in (List, Struct, Unknown)
        and is_polars_dtype(dtype)
        and (python_dtype is None)
    ):
        constructor = polars_type_to_constructor(dtype)
        pyseries = _construct_series_with_fallbacks(
            constructor, name, values, dtype, strict=strict
        )
        if dtype in (Date, Datetime, Duration, Time, Categorical, Boolean):
            if pyseries.dtype() != dtype:
                pyseries = pyseries.cast(dtype, strict=True)
        return pyseries

    elif dtype == Struct:
        struct_schema = dtype.to_schema() if isinstance(dtype, Struct) else None
        empty = {}  # type: ignore[var-annotated]
        return sequence_to_pydf(
            data=[(empty if v is None else v) for v in values],
            schema=struct_schema,
            orient="row",
        ).to_struct(name)
    else:
        if python_dtype is None:
            if value is None:
                # Create a series with a dtype_if_empty dtype (if set) or Float32
                # (if not set) for a sequence which contains only None values.
                constructor = polars_type_to_constructor(
                    dtype_if_empty if dtype_if_empty else Float32
                )
                return _construct_series_with_fallbacks(
                    constructor, name, values, dtype, strict=strict
                )

            # generic default dtype
            python_dtype = type(value)

        # temporal branch
        if python_dtype in py_temporal_types:
            if dtype is None:
                dtype = py_type_to_dtype(python_dtype)  # construct from integer
            elif dtype in py_temporal_types:
                dtype = py_type_to_dtype(dtype)

            values_dtype = (
                None
                if value is None
                else py_type_to_dtype(type(value), raise_unmatched=False)
            )
            if values_dtype in FLOAT_DTYPES:
                raise TypeError(
                    # we do not accept float values as temporal; if this is
                    # required, the caller should explicitly cast to int first.
                    f"'float' object cannot be interpreted as a {python_dtype.__name__!r}"
                )

            # we use anyvalue builder to create the datetime array
            # we store the values internally as UTC and set the timezone
            py_series = PySeries.new_from_anyvalues(name, values, strict)
            time_unit = getattr(dtype, "time_unit", None)
            if time_unit is None:
                s = wrap_s(py_series)
            else:
                s = wrap_s(py_series).dt.cast_time_unit(time_unit)
            time_zone = getattr(dtype, "time_zone", None)
            if dtype == Datetime and (
                value.tzinfo is not None or time_zone is not None
            ):
                values_tz = str(value.tzinfo) if value.tzinfo is not None else None
                dtype_tz = dtype.time_zone  # type: ignore[union-attr]
                if values_tz is not None and (
                    dtype_tz is not None and dtype_tz != "UTC"
                ):
                    raise ValueError(
                        "time-zone-aware datetimes are converted to UTC. "
                        "Please either drop the time zone from the dtype, "
                        "or set it to 'UTC'. To convert to a different time zone, "
                        "please use `.dt.convert_time_zone`"
                    )
                if values_tz != "UTC" and dtype_tz is None:
                    warnings.warn(
                        "Constructing a Series with time-zone-aware "
                        "datetimes results in a Series with UTC time zone. "
                        "To silence this warning, you can filter "
                        "warnings of class TimeZoneAwareConstructorWarning, or "
                        "set 'UTC' as the time zone of your datatype.",
                        TimeZoneAwareConstructorWarning,
                        stacklevel=find_stacklevel(),
                    )
                return s.dt.replace_time_zone(dtype_tz or "UTC")._s
            return s._s

        elif (
            _check_for_numpy(value)
            and isinstance(value, np.ndarray)
            and len(value.shape) == 1
        ):
            return PySeries.new_series_list(
                name,
                [
                    numpy_to_pyseries("", v, strict=strict, nan_to_null=nan_to_null)
                    for v in values
                ],
                strict,
            )

        elif python_dtype in (list, tuple):
            if isinstance(dtype, Object):
                return PySeries.new_object(name, values, strict)
            if dtype:
                srs = sequence_from_anyvalue_or_object(name, values)
                if dtype.is_not(srs.dtype()):
                    srs = srs.cast(dtype, strict=False)
                return srs
            return sequence_from_anyvalue_or_object(name, values)

        elif python_dtype == pl.Series:
            return PySeries.new_series_list(name, [v._s for v in values], strict)

        elif python_dtype == PySeries:
            return PySeries.new_series_list(name, values, strict)
        else:
            constructor = py_type_to_constructor(python_dtype)
            if constructor == PySeries.new_object:
                try:
                    return PySeries.new_from_anyvalues(name, values, strict)
                # raised if we cannot convert to Wrap<AnyValue>
                except RuntimeError:
                    return sequence_from_anyvalue_or_object(name, values)

            return _construct_series_with_fallbacks(
                constructor, name, values, dtype, strict=strict
            )
