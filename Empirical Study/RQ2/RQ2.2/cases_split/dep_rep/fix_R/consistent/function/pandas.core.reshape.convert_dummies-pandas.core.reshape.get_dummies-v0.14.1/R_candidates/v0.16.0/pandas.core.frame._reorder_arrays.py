def _reorder_arrays(arrays, arr_columns, columns):
    # reorder according to the columns
    if (columns is not None and len(columns) and arr_columns is not None and
            len(arr_columns)):
        indexer = _ensure_index(
            arr_columns).get_indexer(columns)
        arr_columns = _ensure_index(
            [arr_columns[i] for i in indexer])
        arrays = [arrays[i] for i in indexer]
    return arrays, arr_columns
