def describe(a, axis=0):
    """
    Computes several descriptive statistics of the passed array.

    Parameters
    ----------
    a : array

    axis : int or None

    Returns
    -------
    n : int
        (size of the data (discarding missing values)
    mm : (int, int)
        min, max

    arithmetic mean : float

    unbiased variance : float

    biased skewness : float

    biased kurtosis : float

    Examples
    --------

    >>> ma = np.ma.array(range(6), mask=[0, 0, 0, 1, 1, 1])
    >>> describe(ma)
    (array(3),
     (0, 2),
     1.0,
     1.0,
     masked_array(data = 0.0,
                 mask = False,
           fill_value = 1e+20)
    ,
     -1.5)

    """
    a, axis = _chk_asarray(a, axis)
    n = a.count(axis)
    mm = (ma.minimum.reduce(a), ma.maximum.reduce(a))
    m = a.mean(axis)
    v = a.var(axis)
    sk = skew(a, axis)
    kurt = kurtosis(a, axis)
    return n, mm, m, v, sk, kurt
