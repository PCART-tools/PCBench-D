def _isnull_new(obj):
    if lib.isscalar(obj):
        return lib.checknull(obj)
    # hack (for now) because MI registers as ndarray
    elif isinstance(obj, pd.MultiIndex):
        raise NotImplementedError("isnull is not defined for MultiIndex")
    elif isinstance(obj, (ABCSeries, np.ndarray, pd.Index)):
        return _isnull_ndarraylike(obj)
    elif isinstance(obj, ABCGeneric):
        return obj._constructor(obj._data.isnull(func=isnull))
    elif isinstance(obj, list) or hasattr(obj, '__array__'):
        return _isnull_ndarraylike(np.asarray(obj))
    else:
        return obj is None
