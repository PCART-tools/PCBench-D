def unique1d(values):
    """
    Hash table-based unique
    """
    if np.issubdtype(values.dtype, np.floating):
        table = _hash.Float64HashTable(len(values))
        uniques = np.array(table.unique(_ensure_float64(values)),
                           dtype=np.float64)
    elif np.issubdtype(values.dtype, np.datetime64):
        table = _hash.Int64HashTable(len(values))
        uniques = table.unique(_ensure_int64(values))
        uniques = uniques.view('M8[ns]')
    elif np.issubdtype(values.dtype, np.timedelta64):
        table = _hash.Int64HashTable(len(values))
        uniques = table.unique(_ensure_int64(values))
        uniques = uniques.view('m8[ns]')
    elif np.issubdtype(values.dtype, np.integer):
        table = _hash.Int64HashTable(len(values))
        uniques = table.unique(_ensure_int64(values))
    else:
        table = _hash.PyObjectHashTable(len(values))
        uniques = table.unique(_ensure_object(values))
    return uniques
