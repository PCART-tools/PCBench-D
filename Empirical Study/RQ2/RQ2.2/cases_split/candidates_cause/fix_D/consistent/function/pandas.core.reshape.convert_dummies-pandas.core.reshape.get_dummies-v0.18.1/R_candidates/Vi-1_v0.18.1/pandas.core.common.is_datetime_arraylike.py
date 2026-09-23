def is_datetime_arraylike(arr):
    """ return if we are datetime arraylike / DatetimeIndex """
    if isinstance(arr, gt.ABCDatetimeIndex):
        return True
    elif isinstance(arr, (np.ndarray, gt.ABCSeries)):
        return arr.dtype == object and lib.infer_dtype(arr) == 'datetime'
    return getattr(arr, 'inferred_type', None) == 'datetime'
