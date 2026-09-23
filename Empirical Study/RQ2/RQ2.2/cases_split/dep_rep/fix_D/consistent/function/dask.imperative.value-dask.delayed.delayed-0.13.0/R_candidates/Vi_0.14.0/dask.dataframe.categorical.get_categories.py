def get_categories(x, object_only=False):
    """Return a dask object to compute the categoricals for `x`. Returns None
    if already a known categorical"""
    if is_categorical_dtype(x):
        return (None if has_known_categories(x) else
                x.map_partitions(_get_categories).unique().values)
    return (x.dropna().drop_duplicates()
            if not object_only or x.dtype == object else None)
