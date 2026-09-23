def _list_of_series_to_arrays(data, columns, coerce_float=False, dtype=None):
    from pandas.core.index import _get_combined_index

    if columns is None:
        columns = _get_combined_index([
            s.index for s in data if getattr(s, 'index', None) is not None
        ])

    indexer_cache = {}

    aligned_values = []
    for s in data:
        index = getattr(s, 'index', None)
        if index is None:
            index = _default_index(len(s))

        if id(index) in indexer_cache:
            indexer = indexer_cache[id(index)]
        else:
            indexer = indexer_cache[id(index)] = index.get_indexer(columns)

        values = _values_from_object(s)
        aligned_values.append(com.take_1d(values, indexer))

    values = np.vstack(aligned_values)

    if values.dtype == np.object_:
        content = list(values.T)
        return _convert_object_array(content, columns, dtype=dtype,
                                     coerce_float=coerce_float)
    else:
        return values.T, columns
