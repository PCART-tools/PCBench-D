def str_split(arr, pat=None, n=None):
    """
    Split each string (a la re.split) in the Series/Index by given
    pattern, propagating NA values. Equivalent to :meth:`str.split`.

    Parameters
    ----------
    pat : string, default None
        String or regular expression to split on. If None, splits on whitespace
    n : int, default -1 (all)
        None, 0 and -1 will be interpreted as return all splits
    expand : bool, default False
        * If True, return DataFrame/MultiIndex expanding dimensionality.
        * If False, return Series/Index.

        .. versionadded:: 0.16.1
    return_type : deprecated, use `expand`

    Returns
    -------
    split : Series/Index or DataFrame/MultiIndex of objects
    """
    if pat is None:
        if n is None or n == 0:
            n = -1
        f = lambda x: x.split(pat, n)
    else:
        if len(pat) == 1:
            if n is None or n == 0:
                n = -1
            f = lambda x: x.split(pat, n)
        else:
            if n is None or n == -1:
                n = 0
            regex = re.compile(pat)
            f = lambda x: regex.split(x, maxsplit=n)
    res = _na_map(f, arr)
    return res
