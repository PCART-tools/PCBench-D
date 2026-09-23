def _isnull_old(obj):
    """Detect missing values. Treat None, NaN, INF, -INF as null.

    Parameters
    ----------
    arr: ndarray or object value

    Returns
    -------
    boolean ndarray or boolean
    """
    if lib.isscalar(obj):
        return lib.checknull_old(obj)
    # hack (for now) because MI registers as ndarray
    elif isinstance(obj, pd.MultiIndex):
        raise NotImplementedError("isnull is not defined for MultiIndex")
    elif isinstance(obj, (gt.ABCSeries, np.ndarray, pd.Index)):
        return _isnull_ndarraylike_old(obj)
    elif isinstance(obj, gt.ABCGeneric):
        return obj._constructor(obj._data.isnull(func=_isnull_old))
    elif isinstance(obj, list) or hasattr(obj, '__array__'):
        return _isnull_ndarraylike_old(np.asarray(obj))
    else:
        return obj is None
