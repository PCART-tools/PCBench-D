def take_2d_multi(arr, indexer, out=None, fill_value=np.nan, mask_info=None,
                  allow_fill=True):
    """
    Specialized Cython take which sets NaN values in one pass
    """
    if indexer is None or (indexer[0] is None and indexer[1] is None):
        row_idx = np.arange(arr.shape[0], dtype=np.int64)
        col_idx = np.arange(arr.shape[1], dtype=np.int64)
        indexer = row_idx, col_idx
        dtype, fill_value = arr.dtype, arr.dtype.type()
    else:
        row_idx, col_idx = indexer
        if row_idx is None:
            row_idx = np.arange(arr.shape[0], dtype=np.int64)
        else:
            row_idx = _ensure_int64(row_idx)
        if col_idx is None:
            col_idx = np.arange(arr.shape[1], dtype=np.int64)
        else:
            col_idx = _ensure_int64(col_idx)
        indexer = row_idx, col_idx
        if not allow_fill:
            dtype, fill_value = arr.dtype, arr.dtype.type()
            mask_info = None, False
        else:
            # check for promotion based on types only (do this first because
            # it's faster than computing a mask)
            dtype, fill_value = _maybe_promote(arr.dtype, fill_value)
            if dtype != arr.dtype and (out is None or out.dtype != dtype):
                # check if promotion is actually required based on indexer
                if mask_info is not None:
                    (row_mask, col_mask), (row_needs, col_needs) = mask_info
                else:
                    row_mask = row_idx == -1
                    col_mask = col_idx == -1
                    row_needs = row_mask.any()
                    col_needs = col_mask.any()
                    mask_info = (row_mask, col_mask), (row_needs, col_needs)
                if row_needs or col_needs:
                    if out is not None and out.dtype != dtype:
                        raise TypeError('Incompatible type for fill_value')
                else:
                    # if not, then depromote, set fill_value to dummy
                    # (it won't be used but we don't want the cython code
                    # to crash when trying to cast it to dtype)
                    dtype, fill_value = arr.dtype, arr.dtype.type()

    # at this point, it's guaranteed that dtype can hold both the arr values
    # and the fill_value
    if out is None:
        out_shape = len(row_idx), len(col_idx)
        out = np.empty(out_shape, dtype=dtype)

    func = _take_2d_multi_dict.get((arr.dtype.name, out.dtype.name), None)
    if func is None and arr.dtype != out.dtype:
        func = _take_2d_multi_dict.get((out.dtype.name, out.dtype.name), None)
        if func is not None:
            func = _convert_wrapper(func, out.dtype)
    if func is None:

        def func(arr, indexer, out, fill_value=np.nan):
            _take_2d_multi_generic(arr, indexer, out, fill_value=fill_value,
                                   mask_info=mask_info)

    func(arr, indexer, out=out, fill_value=fill_value)
    return out
