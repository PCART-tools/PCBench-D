def is_period_arraylike(arr):
    """ return if we are period arraylike / PeriodIndex """
    if isinstance(arr, pd.PeriodIndex):
        return True
    elif isinstance(arr, (np.ndarray, gt.ABCSeries)):
        return arr.dtype == object and lib.infer_dtype(arr) == 'period'
    return getattr(arr, 'inferred_type', None) == 'period'
