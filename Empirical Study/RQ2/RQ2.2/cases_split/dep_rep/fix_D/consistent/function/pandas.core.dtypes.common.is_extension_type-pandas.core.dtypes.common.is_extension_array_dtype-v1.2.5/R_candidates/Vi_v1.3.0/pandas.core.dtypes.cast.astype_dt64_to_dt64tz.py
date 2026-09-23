def astype_dt64_to_dt64tz(
    values: ArrayLike, dtype: DtypeObj, copy: bool, via_utc: bool = False
) -> DatetimeArray:
    # GH#33401 we have inconsistent behaviors between
    #  Datetimeindex[naive].astype(tzaware)
    #  Series[dt64].astype(tzaware)
    # This collects them in one place to prevent further fragmentation.

    from pandas.core.construction import ensure_wrapped_if_datetimelike

    values = ensure_wrapped_if_datetimelike(values)
    values = cast("DatetimeArray", values)
    aware = isinstance(dtype, DatetimeTZDtype)

    if via_utc:
        # Series.astype behavior

        # caller is responsible for checking this
        assert values.tz is None and aware
        dtype = cast(DatetimeTZDtype, dtype)

        if copy:
            # this should be the only copy
            values = values.copy()

        level = find_stack_level()
        warnings.warn(
            "Using .astype to convert from timezone-naive dtype to "
            "timezone-aware dtype is deprecated and will raise in a "
            "future version.  Use ser.dt.tz_localize instead.",
            FutureWarning,
            stacklevel=level,
        )

        # FIXME: GH#33401 this doesn't match DatetimeArray.astype, which
        #  goes through the `not via_utc` path
        return values.tz_localize("UTC").tz_convert(dtype.tz)

    else:
        # DatetimeArray/DatetimeIndex.astype behavior
        if values.tz is None and aware:
            dtype = cast(DatetimeTZDtype, dtype)
            level = find_stack_level()
            warnings.warn(
                "Using .astype to convert from timezone-naive dtype to "
                "timezone-aware dtype is deprecated and will raise in a "
                "future version.  Use obj.tz_localize instead.",
                FutureWarning,
                stacklevel=level,
            )

            return values.tz_localize(dtype.tz)

        elif aware:
            # GH#18951: datetime64_tz dtype but not equal means different tz
            dtype = cast(DatetimeTZDtype, dtype)
            result = values.tz_convert(dtype.tz)
            if copy:
                result = result.copy()
            return result

        elif values.tz is not None:
            level = find_stack_level()
            warnings.warn(
                "Using .astype to convert from timezone-aware dtype to "
                "timezone-naive dtype is deprecated and will raise in a "
                "future version.  Use obj.tz_localize(None) or "
                "obj.tz_convert('UTC').tz_localize(None) instead",
                FutureWarning,
                stacklevel=level,
            )

            result = values.tz_convert("UTC").tz_localize(None)
            if copy:
                result = result.copy()
            return result

        raise NotImplementedError("dtype_equal case should be handled elsewhere")
