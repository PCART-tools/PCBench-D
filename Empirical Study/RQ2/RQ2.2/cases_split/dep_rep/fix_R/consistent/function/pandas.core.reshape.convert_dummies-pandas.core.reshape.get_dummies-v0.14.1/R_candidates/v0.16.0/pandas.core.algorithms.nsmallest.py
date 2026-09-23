def nsmallest(arr, n, take_last=False):
    '''
    Find the indices of the n smallest values of a numpy array.

    Note: Fails silently with NaN.

    '''
    if take_last:
        arr = arr[::-1]

    narr = len(arr)
    n = min(n, narr)

    sdtype = str(arr.dtype)
    arr = arr.view(_dtype_map.get(sdtype, sdtype))

    kth_val = algos.kth_smallest(arr.copy(), n - 1)
    return _finalize_nsmallest(arr, kth_val, n, take_last, narr)
