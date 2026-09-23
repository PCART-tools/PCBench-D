def _concat_sparse(to_concat, axis=0, typs=None):
    """
    provide concatenation of an sparse/dense array of arrays each of which is a
    single dtype

    Parameters
    ----------
    to_concat : array of arrays
    axis : axis to provide concatenation
    typs : set of to_concat dtypes

    Returns
    -------
    a single array, preserving the combined dtypes
    """

    from pandas.core.arrays import SparseArray

    fill_values = [x.fill_value for x in to_concat if isinstance(x, SparseArray)]
    fill_value = fill_values[0]

    # TODO: Fix join unit generation so we aren't passed this.
    to_concat = [
        x
        if isinstance(x, SparseArray)
        else SparseArray(x.squeeze(), fill_value=fill_value)
        for x in to_concat
    ]

    return SparseArray._concat_same_type(to_concat)
