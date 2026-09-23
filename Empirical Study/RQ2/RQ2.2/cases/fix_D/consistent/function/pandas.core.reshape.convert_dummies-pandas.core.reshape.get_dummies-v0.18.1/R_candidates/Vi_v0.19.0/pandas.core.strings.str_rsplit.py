def str_rsplit(arr, pat=None, n=None):
    """
    Split each string in the Series/Index by the given delimiter
    string, starting at the end of the string and working to the front.
    Equivalent to :meth:`str.rsplit`.

    .. versionadded:: 0.16.2

    Parameters
    ----------
    pat : string, default None
        Separator to split on. If None, splits on whitespace
    n : int, default -1 (all)
        None, 0 and -1 will be interpreted as return all splits
    expand : bool, default False
        * If True, return DataFrame/MultiIndex expanding dimensionality.
        * If False, return Series/Index.

    Returns
    -------
    split : Series/Index or DataFrame/MultiIndex of objects
    """
    if n is None or n == 0:
        n = -1
    f = lambda x: x.rsplit(pat, n)
    res = _na_map(f, arr)
    return res
