def _value_counts_arraylike(values, dropna=True):
    is_datetimetz_type = is_datetimetz(values)
    is_period_type = (is_period_dtype(values) or
                      is_period_arraylike(values))

    orig = values

    from pandas.core.series import Series
    values = Series(values).values
    dtype = values.dtype

    if needs_i8_conversion(dtype) or is_period_type:

        from pandas.tseries.index import DatetimeIndex
        from pandas.tseries.period import PeriodIndex

        if is_period_type:
            # values may be an object
            values = PeriodIndex(values)
            freq = values.freq

        values = values.view(np.int64)
        keys, counts = htable.value_count_int64(values, dropna)

        if dropna:
            msk = keys != iNaT
            keys, counts = keys[msk], counts[msk]

        # convert the keys back to the dtype we came in
        keys = keys.astype(dtype)

        # dtype handling
        if is_datetimetz_type:
            keys = DatetimeIndex._simple_new(keys, tz=orig.dtype.tz)
        if is_period_type:
            keys = PeriodIndex._simple_new(keys, freq=freq)

    elif is_integer_dtype(dtype):
        values = _ensure_int64(values)
        keys, counts = htable.value_count_int64(values, dropna)
    elif is_float_dtype(dtype):
        values = _ensure_float64(values)
        keys, counts = htable.value_count_float64(values, dropna)
    else:
        values = _ensure_object(values)
        mask = isnull(values)
        keys, counts = htable.value_count_object(values, mask)
        if not dropna and mask.any():
            keys = np.insert(keys, 0, np.NaN)
            counts = np.insert(counts, 0, mask.sum())

    return keys, counts
