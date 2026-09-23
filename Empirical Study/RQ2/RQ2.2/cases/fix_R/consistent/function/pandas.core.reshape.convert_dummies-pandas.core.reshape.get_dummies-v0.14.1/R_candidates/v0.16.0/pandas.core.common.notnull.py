def notnull(obj):
    """Replacement for numpy.isfinite / -numpy.isnan which is suitable for use
    on object arrays.

    Parameters
    ----------
    arr : ndarray or object value
        Object to check for *not*-null-ness

    Returns
    -------
    isnulled : array-like of bool or bool
        Array or bool indicating whether an object is *not* null or if an array
        is given which of the element is *not* null.

    See also
    --------
    pandas.isnull : boolean inverse of pandas.notnull
    """
    res = isnull(obj)
    if np.isscalar(res):
        return not res
    return ~res
