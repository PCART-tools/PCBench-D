def str_endswith(arr, pat, na=np.nan):
    """
    Return boolean Series indicating whether each string in the
    Series/Index ends with passed pattern. Equivalent to
    :meth:`str.endswith`.

    Parameters
    ----------
    pat : string
        Character sequence
    na : bool, default NaN

    Returns
    -------
    endswith : Series/array of boolean values
    """
    f = lambda x: x.endswith(pat)
    return _na_map(f, arr, na, dtype=bool)
