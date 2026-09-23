def value_counts(values, sort=True, ascending=False, normalize=False,
                 bins=None, dropna=True):
    """
    Compute a histogram of the counts of non-null values.

    Parameters
    ----------
    values : ndarray (1-d)
    sort : boolean, default True
        Sort by values
    ascending : boolean, default False
        Sort in ascending order
    normalize: boolean, default False
        If True then compute a relative histogram
    bins : integer, optional
        Rather than count values, group them into half-open bins,
        convenience for pd.cut, only works with numeric data
    dropna : boolean, default True
        Don't include counts of NaN

    Returns
    -------
    value_counts : Series

    """
    from pandas.core.series import Series
    from pandas.tools.tile import cut
    from pandas.tseries.period import PeriodIndex

    values = Series(values).values

    if bins is not None:
        try:
            cat, bins = cut(values, bins, retbins=True)
        except TypeError:
            raise TypeError("bins argument only works with numeric data.")
        values = cat.codes

    if com.is_categorical_dtype(values.dtype):
        result = values.value_counts(dropna)

    else:

        dtype = values.dtype
        is_period = com.is_period_arraylike(values)

        if com.is_datetime_or_timedelta_dtype(dtype) or is_period:

            if is_period:
                values = PeriodIndex(values)

            values = values.view(np.int64)
            keys, counts = htable.value_count_int64(values)

            if dropna:
                from pandas.tslib import iNaT
                msk = keys != iNaT
                keys, counts = keys[msk], counts[msk]

            # convert the keys back to the dtype we came in
            keys = keys.astype(dtype)

        elif com.is_integer_dtype(dtype):
            values = com._ensure_int64(values)
            keys, counts = htable.value_count_int64(values)

        else:
            values = com._ensure_object(values)
            mask = com.isnull(values)
            keys, counts = htable.value_count_object(values, mask)
            if not dropna and mask.any():
                keys = np.insert(keys, 0, np.NaN)
                counts = np.insert(counts, 0, mask.sum())

        result = Series(counts, index=com._values_from_object(keys))

        if bins is not None:
            # TODO: This next line should be more efficient
            result = result.reindex(np.arange(len(cat.categories)), fill_value=0)
            result.index = bins[:-1]

    if sort:
        result.sort()
        if not ascending:
            result = result[::-1]

    if normalize:
        result = result / float(values.size)

    return result
