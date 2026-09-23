def take_nd(arr, indexer, axis=0, out=None, fill_value=np.nan,
            mask_info=None, allow_fill=True):
    """
    Specialized Cython take which sets NaN values in one pass

    Parameters
    ----------
    arr : ndarray
        Input array
    indexer : ndarray
        1-D array of indices to take, subarrays corresponding to -1 value
        indicies are filed with fill_value
    axis : int, default 0
        Axis to take from
    out : ndarray or None, default None
        Optional output array, must be appropriate type to hold input and
        fill_value together, if indexer has any -1 value entries; call
        common._maybe_promote to determine this type for any fill_value
    fill_value : any, default np.nan
        Fill value to replace -1 values with
    mask_info : tuple of (ndarray, boolean)
        If provided, value should correspond to:
            (indexer != -1, (indexer != -1).any())
        If not provided, it will be computed internally if necessary
    allow_fill : boolean, default True
        If False, indexer is assumed to contain no -1 values so no filling
        will be done.  This short-circuits computation of a mask.  Result is
        undefined if allow_fill == False and -1 is present in indexer.
    """
    if indexer is None:
        indexer = np.arange(arr.shape[axis], dtype=np.int64)
        dtype, fill_value = arr.dtype, arr.dtype.type()
    else:
        indexer = _ensure_int64(indexer)
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
                    mask, needs_masking = mask_info
                else:
                    mask = indexer == -1
                    needs_masking = mask.any()
                    mask_info = mask, needs_masking
                if needs_masking:
                    if out is not None and out.dtype != dtype:
                        raise TypeError('Incompatible type for fill_value')
                else:
                    # if not, then depromote, set fill_value to dummy
                    # (it won't be used but we don't want the cython code
                    # to crash when trying to cast it to dtype)
                    dtype, fill_value = arr.dtype, arr.dtype.type()

    flip_order = False
    if arr.ndim == 2:
        if arr.flags.f_contiguous:
            flip_order = True

    if flip_order:
        arr = arr.T
        axis = arr.ndim - axis - 1
        if out is not None:
            out = out.T

    # at this point, it's guaranteed that dtype can hold both the arr values
    # and the fill_value
    if out is None:
        out_shape = list(arr.shape)
        out_shape[axis] = len(indexer)
        out_shape = tuple(out_shape)
        if arr.flags.f_contiguous and axis == arr.ndim - 1:
            # minor tweak that can make an order-of-magnitude difference
            # for dataframes initialized directly from 2-d ndarrays
            # (s.t. df.values is c-contiguous and df._data.blocks[0] is its
            # f-contiguous transpose)
            out = np.empty(out_shape, dtype=dtype, order='F')
        else:
            out = np.empty(out_shape, dtype=dtype)

    func = _get_take_nd_function(arr.ndim, arr.dtype, out.dtype,
                                 axis=axis, mask_info=mask_info)

    indexer = _ensure_int64(indexer)
    func(arr, indexer, out, fill_value)

    if flip_order:
        out = out.T
    return out
