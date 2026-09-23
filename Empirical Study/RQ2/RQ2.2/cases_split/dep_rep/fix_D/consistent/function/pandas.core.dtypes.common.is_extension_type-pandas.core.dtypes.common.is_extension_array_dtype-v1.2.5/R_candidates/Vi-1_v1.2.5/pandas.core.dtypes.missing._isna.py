def _isna(obj, inf_as_na: bool = False):
    """
    Detect missing values, treating None, NaN or NA as null. Infinite
    values will also be treated as null if inf_as_na is True.

    Parameters
    ----------
    obj: ndarray or object value
        Input array or scalar value.
    inf_as_na: bool
        Whether to treat infinity as null.

    Returns
    -------
    boolean ndarray or boolean
    """
    if is_scalar(obj):
        if inf_as_na:
            return libmissing.checknull_old(obj)
        else:
            return libmissing.checknull(obj)
    # hack (for now) because MI registers as ndarray
    elif isinstance(obj, ABCMultiIndex):
        raise NotImplementedError("isna is not defined for MultiIndex")
    elif isinstance(obj, type):
        return False
    elif isinstance(obj, (ABCSeries, np.ndarray, ABCIndexClass, ABCExtensionArray)):
        return _isna_ndarraylike(obj, inf_as_na=inf_as_na)
    elif isinstance(obj, ABCDataFrame):
        return obj.isna()
    elif isinstance(obj, list):
        return _isna_ndarraylike(np.asarray(obj, dtype=object), inf_as_na=inf_as_na)
    elif hasattr(obj, "__array__"):
        return _isna_ndarraylike(np.asarray(obj), inf_as_na=inf_as_na)
    else:
        return False
