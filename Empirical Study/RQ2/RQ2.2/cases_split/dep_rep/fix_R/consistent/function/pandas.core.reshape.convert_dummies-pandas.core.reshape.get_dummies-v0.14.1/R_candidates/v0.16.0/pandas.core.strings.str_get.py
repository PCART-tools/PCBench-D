def str_get(arr, i):
    """
    Extract element from lists, tuples, or strings in each element in the array

    Parameters
    ----------
    i : int
        Integer index (location)

    Returns
    -------
    items : array
    """
    f = lambda x: x[i] if len(x) > i else np.nan
    return _na_map(f, arr)
