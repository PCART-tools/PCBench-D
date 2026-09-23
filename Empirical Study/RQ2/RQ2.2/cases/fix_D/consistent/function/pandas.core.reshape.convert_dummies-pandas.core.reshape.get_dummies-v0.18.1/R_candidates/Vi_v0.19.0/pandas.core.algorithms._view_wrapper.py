def _view_wrapper(f, arr_dtype=None, out_dtype=None, fill_wrap=None):
    def wrapper(arr, indexer, out, fill_value=np.nan):
        if arr_dtype is not None:
            arr = arr.view(arr_dtype)
        if out_dtype is not None:
            out = out.view(out_dtype)
        if fill_wrap is not None:
            fill_value = fill_wrap(fill_value)
        f(arr, indexer, out, fill_value=fill_value)

    return wrapper
