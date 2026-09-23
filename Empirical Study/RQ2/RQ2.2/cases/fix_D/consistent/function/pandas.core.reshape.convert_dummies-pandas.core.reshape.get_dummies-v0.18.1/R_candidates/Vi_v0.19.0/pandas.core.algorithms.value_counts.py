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
    name = getattr(values, 'name', None)

    if bins is not None:
        try:
            from pandas.tools.tile import cut
            values = Series(values).values
            cat, bins = cut(values, bins, retbins=True)
        except TypeError:
            raise TypeError("bins argument only works with numeric data.")
        values = cat.codes

    if is_extension_type(values) and not is_datetimetz(values):
        # handle Categorical and sparse,
        # datetime tz can be handeled in ndarray path
        result = Series(values).values.value_counts(dropna=dropna)
        result.name = name
        counts = result.values
    else:
        # ndarray path. pass original to handle DatetimeTzBlock
        keys, counts = _value_counts_arraylike(values, dropna=dropna)

        from pandas import Index, Series
        if not isinstance(keys, Index):
            keys = Index(keys)
        result = Series(counts, index=keys, name=name)

    if bins is not None:
        # TODO: This next line should be more efficient
        result = result.reindex(np.arange(len(cat.categories)),
                                fill_value=0)
        result.index = bins[:-1]

    if sort:
        result = result.sort_values(ascending=ascending)

    if normalize:
        result = result / float(counts.sum())

    return result
