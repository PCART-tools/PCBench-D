def _maybe_numeric_slice(df, slice_, include_bool=False):
    """
    want nice defaults for background_gradient that don't break
    with non-numeric data. But if slice_ is passed go with that.
    """
    if slice_ is None:
        dtypes = [np.number]
        if include_bool:
            dtypes.append(bool)
        slice_ = IndexSlice[:, df.select_dtypes(include=dtypes).columns]
    return slice_
