def str_split(arr, pat=None, n=None, return_type='series'):
    """
    Split each string (a la re.split) in array by given pattern, propagating NA
    values

    Parameters
    ----------
    pat : string, default None
        String or regular expression to split on. If None, splits on whitespace
    n : int, default None (all)
    return_type : {'series', 'frame'}, default 'series
        If frame, returns a DataFrame (elements are strings)
        If series, returns an Series (elements are lists of strings).

    Notes
    -----
    Both 0 and -1 will be interpreted as return all splits

    Returns
    -------
    split : array
    """
    from pandas.core.series import Series
    from pandas.core.frame import DataFrame

    if return_type not in ('series', 'frame'):
        raise ValueError("return_type must be {'series', 'frame'}")
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
    if return_type == 'frame':
        res = DataFrame((Series(x) for x in _na_map(f, arr)), index=arr.index)
    else:
        res = _na_map(f, arr)
    return res
