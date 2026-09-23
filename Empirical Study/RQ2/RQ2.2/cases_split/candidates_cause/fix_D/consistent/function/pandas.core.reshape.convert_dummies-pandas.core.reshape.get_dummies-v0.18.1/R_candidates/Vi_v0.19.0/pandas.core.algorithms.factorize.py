def factorize(values, sort=False, order=None, na_sentinel=-1, size_hint=None):
    """
    Encode input values as an enumerated type or categorical variable

    Parameters
    ----------
    values : ndarray (1-d)
        Sequence
    sort : boolean, default False
        Sort by values
    na_sentinel : int, default -1
        Value to mark "not found"
    size_hint : hint to the hashtable sizer

    Returns
    -------
    labels : the indexer to the original array
    uniques : ndarray (1-d) or Index
        the unique values. Index is returned when passed values is Index or
        Series

    note: an array of Periods will ignore sort as it returns an always sorted
    PeriodIndex
    """
    from pandas import Index, Series, DatetimeIndex

    vals = np.asarray(values)

    # localize to UTC
    is_datetimetz_type = is_datetimetz(values)
    if is_datetimetz_type:
        values = DatetimeIndex(values)
        vals = values.asi8

    is_datetime = is_datetime64_dtype(vals)
    is_timedelta = is_timedelta64_dtype(vals)
    (hash_klass, vec_klass), vals = _get_data_algo(vals, _hashtables)

    table = hash_klass(size_hint or len(vals))
    uniques = vec_klass()
    labels = table.get_labels(vals, uniques, 0, na_sentinel, True)

    labels = _ensure_platform_int(labels)

    uniques = uniques.to_array()

    if sort and len(uniques) > 0:
        uniques, labels = safe_sort(uniques, labels, na_sentinel=na_sentinel,
                                    assume_unique=True)

    if is_datetimetz_type:
        # reset tz
        uniques = values._shallow_copy(uniques)
    elif is_datetime:
        uniques = uniques.astype('M8[ns]')
    elif is_timedelta:
        uniques = uniques.astype('m8[ns]')
    if isinstance(values, Index):
        uniques = values._shallow_copy(uniques, name=None)
    elif isinstance(values, Series):
        uniques = Index(uniques)
    return labels, uniques
