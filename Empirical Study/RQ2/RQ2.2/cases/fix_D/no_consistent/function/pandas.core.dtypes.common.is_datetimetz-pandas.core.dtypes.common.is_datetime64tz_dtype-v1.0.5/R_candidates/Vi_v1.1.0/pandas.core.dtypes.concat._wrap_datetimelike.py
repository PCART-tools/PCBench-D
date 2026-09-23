def _wrap_datetimelike(arr):
    """
    Wrap datetime64 and timedelta64 ndarrays in DatetimeArray/TimedeltaArray.

    DTA/TDA handle .astype(object) correctly.
    """
    from pandas.core.construction import array as pd_array, extract_array

    arr = extract_array(arr, extract_numpy=True)
    if isinstance(arr, np.ndarray) and arr.dtype.kind in ["m", "M"]:
        arr = pd_array(arr)
    return arr
