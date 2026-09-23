def _where_compat(mask, arr1, arr2):
    if arr1.dtype == _NS_DTYPE and arr2.dtype == _NS_DTYPE:
        new_vals = np.where(mask, arr1.view('i8'), arr2.view('i8'))
        return new_vals.view(_NS_DTYPE)

    import pandas.tslib as tslib
    if arr1.dtype == _NS_DTYPE:
        arr1 = tslib.ints_to_pydatetime(arr1.view('i8'))
    if arr2.dtype == _NS_DTYPE:
        arr2 = tslib.ints_to_pydatetime(arr2.view('i8'))

    return np.where(mask, arr1, arr2)
