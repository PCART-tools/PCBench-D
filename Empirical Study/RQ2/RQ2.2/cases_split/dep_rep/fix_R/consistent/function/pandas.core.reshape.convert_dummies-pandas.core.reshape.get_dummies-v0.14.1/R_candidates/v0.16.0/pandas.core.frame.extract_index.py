def extract_index(data):
    from pandas.core.index import _union_indexes

    index = None
    if len(data) == 0:
        index = Index([])
    elif len(data) > 0:
        raw_lengths = []
        indexes = []

        have_raw_arrays = False
        have_series = False
        have_dicts = False

        for v in data:
            if isinstance(v, Series):
                have_series = True
                indexes.append(v.index)
            elif isinstance(v, dict):
                have_dicts = True
                indexes.append(list(v.keys()))
            elif is_list_like(v) and getattr(v, 'ndim', 1) == 1:
                have_raw_arrays = True
                raw_lengths.append(len(v))

        if not indexes and not raw_lengths:
            raise ValueError('If using all scalar values, you must pass'
                             ' an index')

        if have_series or have_dicts:
            index = _union_indexes(indexes)

        if have_raw_arrays:
            lengths = list(set(raw_lengths))
            if len(lengths) > 1:
                raise ValueError('arrays must all be same length')

            if have_dicts:
                raise ValueError('Mixing dicts with non-Series may lead to '
                                 'ambiguous ordering.')

            if have_series:
                if lengths[0] != len(index):
                    msg = ('array length %d does not match index length %d'
                           % (lengths[0], len(index)))
                    raise ValueError(msg)
            else:
                index = Index(np.arange(lengths[0]))

    return _ensure_index(index)
