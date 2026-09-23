def maybe_cast_to_datetime(
    value: ExtensionArray | np.ndarray | list, dtype: DtypeObj | None
) -> ExtensionArray | np.ndarray:
    """
    try to cast the array/value to a datetimelike dtype, converting float
    nan to iNaT

    We allow a list *only* when dtype is not None.
    """
    from pandas.core.arrays.datetimes import sequence_to_datetimes
    from pandas.core.arrays.timedeltas import TimedeltaArray

    if not is_list_like(value):
        raise TypeError("value must be listlike")

    if is_timedelta64_dtype(dtype):
        # TODO: _from_sequence would raise ValueError in cases where
        #  ensure_nanosecond_dtype raises TypeError
        dtype = cast(np.dtype, dtype)
        dtype = ensure_nanosecond_dtype(dtype)
        res = TimedeltaArray._from_sequence(value, dtype=dtype)
        return res

    if dtype is not None:
        is_datetime64 = is_datetime64_dtype(dtype)
        is_datetime64tz = is_datetime64tz_dtype(dtype)

        vdtype = getattr(value, "dtype", None)

        if is_datetime64 or is_datetime64tz:
            dtype = ensure_nanosecond_dtype(dtype)

            value = np.array(value, copy=False)

            # we have an array of datetime or timedeltas & nulls
            if value.size or not is_dtype_equal(value.dtype, dtype):
                _disallow_mismatched_datetimelike(value, dtype)

                try:
                    if is_datetime64:
                        dta = sequence_to_datetimes(value, allow_object=False)
                        # GH 25843: Remove tz information since the dtype
                        # didn't specify one

                        if dta.tz is not None:
                            warnings.warn(
                                "Data is timezone-aware. Converting "
                                "timezone-aware data to timezone-naive by "
                                "passing dtype='datetime64[ns]' to "
                                "DataFrame or Series is deprecated and will "
                                "raise in a future version. Use "
                                "`pd.Series(values).dt.tz_localize(None)` "
                                "instead.",
                                FutureWarning,
                                stacklevel=8,
                            )
                            # equiv: dta.view(dtype)
                            # Note: NOT equivalent to dta.astype(dtype)
                            dta = dta.tz_localize(None)

                        value = dta
                    elif is_datetime64tz:
                        dtype = cast(DatetimeTZDtype, dtype)
                        # The string check can be removed once issue #13712
                        # is solved. String data that is passed with a
                        # datetime64tz is assumed to be naive which should
                        # be localized to the timezone.
                        is_dt_string = is_string_dtype(value.dtype)
                        dta = sequence_to_datetimes(value, allow_object=False)
                        if dta.tz is not None:
                            value = dta.astype(dtype, copy=False)
                        elif is_dt_string:
                            # Strings here are naive, so directly localize
                            # equiv: dta.astype(dtype)  # though deprecated

                            value = dta.tz_localize(dtype.tz)
                        else:
                            # Numeric values are UTC at this point,
                            # so localize and convert
                            # equiv: Series(dta).astype(dtype) # though deprecated
                            if getattr(vdtype, "kind", None) == "M":
                                # GH#24559, GH#33401 deprecate behavior inconsistent
                                #  with DatetimeArray/DatetimeIndex
                                warnings.warn(
                                    "In a future version, constructing a Series "
                                    "from datetime64[ns] data and a "
                                    "DatetimeTZDtype will interpret the data "
                                    "as wall-times instead of "
                                    "UTC times, matching the behavior of "
                                    "DatetimeIndex. To treat the data as UTC "
                                    "times, use pd.Series(data).dt"
                                    ".tz_localize('UTC').tz_convert(dtype.tz) "
                                    "or pd.Series(data.view('int64'), dtype=dtype)",
                                    FutureWarning,
                                    stacklevel=5,
                                )

                            value = dta.tz_localize("UTC").tz_convert(dtype.tz)
                except OutOfBoundsDatetime:
                    raise
                except ValueError:
                    # TODO(GH#40048): only catch dateutil's ParserError
                    #  once we can reliably import it in all supported versions
                    pass

        elif getattr(vdtype, "kind", None) in ["m", "M"]:
            # we are already datetimelike and want to coerce to non-datetimelike;
            #  astype_nansafe will raise for anything other than object, then upcast.
            #  see test_datetimelike_values_with_object_dtype
            # error: Argument 2 to "astype_nansafe" has incompatible type
            # "Union[dtype[Any], ExtensionDtype]"; expected "dtype[Any]"
            return astype_nansafe(value, dtype)  # type: ignore[arg-type]

    elif isinstance(value, np.ndarray):
        if value.dtype.kind in ["M", "m"]:
            # catch a datetime/timedelta that is not of ns variety
            # and no coercion specified
            value = sanitize_to_nanoseconds(value)

        elif value.dtype == object:
            value = maybe_infer_to_datetimelike(value)

    elif isinstance(value, list):
        # we only get here with dtype=None, which we do not allow
        raise ValueError(
            "maybe_cast_to_datetime allows a list *only* if dtype is not None"
        )

    # at this point we have converted or raised in all cases where we had a list
    return cast(ArrayLike, value)
