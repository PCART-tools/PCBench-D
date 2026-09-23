def str_startswith(arr, pat, na=np.nan):
    """
    Return boolean Series/``array`` indicating whether each string in the
    Series/Index starts with passed pattern. Equivalent to
    :meth:`str.startswith`.

    Parameters
    ----------
    pat : string
        Character sequence
    na : bool, default NaN

    Returns
    -------
    startswith : Series/array of boolean values
    """
    f = lambda x: x.startswith(pat)
    return _na_map(f, arr, na, dtype=bool)
