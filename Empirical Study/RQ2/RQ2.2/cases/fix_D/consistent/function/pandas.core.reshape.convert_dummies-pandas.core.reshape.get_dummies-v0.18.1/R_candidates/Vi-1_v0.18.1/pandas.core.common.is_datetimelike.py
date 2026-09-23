def is_datetimelike(arr):
    return (arr.dtype in _DATELIKE_DTYPES or
            isinstance(arr, gt.ABCPeriodIndex) or
            is_datetimetz(arr))
