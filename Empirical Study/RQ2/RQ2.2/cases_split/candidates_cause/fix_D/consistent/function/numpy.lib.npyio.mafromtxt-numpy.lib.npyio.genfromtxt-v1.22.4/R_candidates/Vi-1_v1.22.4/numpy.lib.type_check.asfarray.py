@array_function_dispatch(_asfarray_dispatcher)
def asfarray(a, dtype=_nx.float_):
    """
    Return an array converted to a float type.

    Parameters
    ----------
    a : array_like
        The input array.
    dtype : str or dtype object, optional
        Float type code to coerce input array `a`.  If `dtype` is one of the
        'int' dtypes, it is replaced with float64.

    Returns
    -------
    out : ndarray
        The input `a` as a float ndarray.

    Examples
    --------
    >>> np.asfarray([2, 3])
    array([2.,  3.])
    >>> np.asfarray([2, 3], dtype='float')
    array([2.,  3.])
    >>> np.asfarray([2, 3], dtype='int8')
    array([2.,  3.])

    """
    if not _nx.issubdtype(dtype, _nx.inexact):
        dtype = _nx.float_
    return asarray(a, dtype=dtype)
