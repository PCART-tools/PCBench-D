def isnull(obj):
    """Detect missing values (NaN in numeric arrays, None/NaN in object arrays)

    Parameters
    ----------
    arr : ndarray or object value
        Object to check for null-ness

    Returns
    -------
    isnulled : array-like of bool or bool
        Array or bool indicating whether an object is null or if an array is
        given which of the element is null.

    See also
    --------
    pandas.notnull: boolean inverse of pandas.isnull
    """
    return _isnull(obj)
