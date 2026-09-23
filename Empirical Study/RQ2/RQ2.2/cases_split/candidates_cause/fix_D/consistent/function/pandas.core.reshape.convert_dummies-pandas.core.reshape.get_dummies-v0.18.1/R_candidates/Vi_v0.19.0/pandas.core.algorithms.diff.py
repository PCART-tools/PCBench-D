def diff(arr, n, axis=0):
    """ difference of n between self,
        analagoust to s-s.shift(n) """

    n = int(n)
    na = np.nan
    dtype = arr.dtype
    is_timedelta = False
    if needs_i8_conversion(arr):
        dtype = np.float64
        arr = arr.view('i8')
        na = tslib.iNaT
        is_timedelta = True
    elif issubclass(dtype.type, np.integer):
        dtype = np.float64
    elif issubclass(dtype.type, np.bool_):
        dtype = np.object_

    dtype = np.dtype(dtype)
    out_arr = np.empty(arr.shape, dtype=dtype)

    na_indexer = [slice(None)] * arr.ndim
    na_indexer[axis] = slice(None, n) if n >= 0 else slice(n, None)
    out_arr[tuple(na_indexer)] = na

    if arr.ndim == 2 and arr.dtype.name in _diff_special:
        f = _diff_special[arr.dtype.name]
        f(arr, out_arr, n, axis)
    else:
        res_indexer = [slice(None)] * arr.ndim
        res_indexer[axis] = slice(n, None) if n >= 0 else slice(None, n)
        res_indexer = tuple(res_indexer)

        lag_indexer = [slice(None)] * arr.ndim
        lag_indexer[axis] = slice(None, -n) if n > 0 else slice(-n, None)
        lag_indexer = tuple(lag_indexer)

        # need to make sure that we account for na for datelike/timedelta
        # we don't actually want to subtract these i8 numbers
        if is_timedelta:
            res = arr[res_indexer]
            lag = arr[lag_indexer]

            mask = (arr[res_indexer] == na) | (arr[lag_indexer] == na)
            if mask.any():
                res = res.copy()
                res[mask] = 0
                lag = lag.copy()
                lag[mask] = 0

            result = res - lag
            result[mask] = na
            out_arr[res_indexer] = result
        else:
            out_arr[res_indexer] = arr[res_indexer] - arr[lag_indexer]

    if is_timedelta:
        from pandas import TimedeltaIndex
        out_arr = TimedeltaIndex(out_arr.ravel().astype('int64')).asi8.reshape(
            out_arr.shape).astype('timedelta64[ns]')

    return out_arr
