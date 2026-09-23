def trim(a, limits=None, inclusive=(True,True), relative=False, axis=None):
    """
    Trims an array by masking the data outside some given limits.

    Returns a masked version of the input array.

    %s

    Examples
    --------
    >>> from scipy.stats.mstats import trim
    >>> z = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10]
    >>> print(trim(z,(3,8)))
    [-- -- 3 4 5 6 7 8 -- --]
    >>> print(trim(z,(0.1,0.2),relative=True))
    [-- 2 3 4 5 6 7 8 -- --]

    """
    if relative:
        return trimr(a, limits=limits, inclusive=inclusive, axis=axis)
    else:
        return trima(a, limits=limits, inclusive=inclusive)
