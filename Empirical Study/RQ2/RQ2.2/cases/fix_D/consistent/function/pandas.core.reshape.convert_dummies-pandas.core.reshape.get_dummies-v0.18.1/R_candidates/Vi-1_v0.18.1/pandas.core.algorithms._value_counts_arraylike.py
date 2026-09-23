def _value_counts_arraylike(values, dropna=True):
    is_datetimetz = com.is_datetimetz(values)
    is_period = (isinstance(values, gt.ABCPeriodIndex) or
                 com.is_period_arraylike(values))

    orig = values

    from pandas.core.series import Series
    values = Series(values).values
    dtype = values.dtype

    if com.is_datetime_or_timedelta_dtype(dtype) or is_period:
        from pandas.tseries.index import DatetimeIndex
        from pandas.tseries.period import PeriodIndex

        if is_period:
            values = PeriodIndex(values)
            freq = values.freq

        values = values.view(np.int64)
        keys, counts = htable.value_count_scalar64(values, dropna)

        if dropna:
            msk = keys != iNaT
            keys, counts = keys[msk], counts[msk]

        # convert the keys back to the dtype we came in
        keys = keys.astype(dtype)

        # dtype handling
        if is_datetimetz:
            if isinstance(orig, gt.ABCDatetimeIndex):
                tz = orig.tz
            else:
                tz = orig.dt.tz
            keys = DatetimeIndex._simple_new(keys, tz=tz)
        if is_period:
            keys = PeriodIndex._simple_new(keys, freq=freq)

    elif com.is_integer_dtype(dtype):
        values = com._ensure_int64(values)
        keys, counts = htable.value_count_scalar64(values, dropna)
    elif com.is_float_dtype(dtype):
        values = com._ensure_float64(values)
        keys, counts = htable.value_count_scalar64(values, dropna)
    else:
        values = com._ensure_object(values)
        mask = com.isnull(values)
        keys, counts = htable.value_count_object(values, mask)
        if not dropna and mask.any():
            keys = np.insert(keys, 0, np.NaN)
            counts = np.insert(counts, 0, mask.sum())

    return keys, counts
