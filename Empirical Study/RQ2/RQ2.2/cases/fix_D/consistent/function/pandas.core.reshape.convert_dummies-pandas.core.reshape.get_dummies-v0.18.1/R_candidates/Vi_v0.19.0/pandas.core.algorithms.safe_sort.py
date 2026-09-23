def safe_sort(values, labels=None, na_sentinel=-1, assume_unique=False):
    """
    Sort ``values`` and reorder corresponding ``labels``.
    ``values`` should be unique if ``labels`` is not None.
    Safe for use with mixed types (int, str), orders ints before strs.

    .. versionadded:: 0.19.0

    Parameters
    ----------
    values : list-like
        Sequence; must be unique if ``labels`` is not None.
    labels : list_like
        Indices to ``values``. All out of bound indices are treated as
        "not found" and will be masked with ``na_sentinel``.
    na_sentinel : int, default -1
        Value in ``labels`` to mark "not found".
        Ignored when ``labels`` is None.
    assume_unique : bool, default False
        When True, ``values`` are assumed to be unique, which can speed up
        the calculation. Ignored when ``labels`` is None.

    Returns
    -------
    ordered : ndarray
        Sorted ``values``
    new_labels : ndarray
        Reordered ``labels``; returned when ``labels`` is not None.

    Raises
    ------
    TypeError
        * If ``values`` is not list-like or if ``labels`` is neither None
        nor list-like
        * If ``values`` cannot be sorted
    ValueError
        * If ``labels`` is not None and ``values`` contain duplicates.
    """
    if not is_list_like(values):
        raise TypeError("Only list-like objects are allowed to be passed to"
                        "safe_sort as values")
    values = np.array(values, copy=False)

    def sort_mixed(values):
        # order ints before strings, safe in py3
        str_pos = np.array([isinstance(x, string_types) for x in values],
                           dtype=bool)
        nums = np.sort(values[~str_pos])
        strs = np.sort(values[str_pos])
        return _ensure_object(np.concatenate([nums, strs]))

    sorter = None
    if compat.PY3 and lib.infer_dtype(values) == 'mixed-integer':
        # unorderable in py3 if mixed str/int
        ordered = sort_mixed(values)
    else:
        try:
            sorter = values.argsort()
            ordered = values.take(sorter)
        except TypeError:
            # try this anyway
            ordered = sort_mixed(values)

    # labels:

    if labels is None:
        return ordered

    if not is_list_like(labels):
        raise TypeError("Only list-like objects or None are allowed to be"
                        "passed to safe_sort as labels")
    labels = _ensure_platform_int(np.asarray(labels))

    from pandas import Index
    if not assume_unique and not Index(values).is_unique:
        raise ValueError("values should be unique if labels is not None")

    if sorter is None:
        # mixed types
        (hash_klass, _), values = _get_data_algo(values, _hashtables)
        t = hash_klass(len(values))
        t.map_locations(values)
        sorter = _ensure_platform_int(t.lookup(ordered))

    reverse_indexer = np.empty(len(sorter), dtype=np.int_)
    reverse_indexer.put(sorter, np.arange(len(sorter)))

    mask = (labels < -len(values)) | (labels >= len(values)) | \
        (labels == na_sentinel)

    # (Out of bound indices will be masked with `na_sentinel` next, so we may
    # deal with them here without performance loss using `mode='wrap'`.)
    new_labels = reverse_indexer.take(labels, mode='wrap')
    np.putmask(new_labels, mask, na_sentinel)

    return ordered, _ensure_platform_int(new_labels)
