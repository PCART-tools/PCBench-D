def _c_int_array(
    data: np.ndarray
) -> Tuple[_ctypes_int_ptr, int, np.ndarray]:
    """Get pointer of int numpy array / list."""
    if _is_1d_list(data):
        data = np.array(data, copy=False)
    if _is_numpy_1d_array(data):
        data = _convert_from_sliced_object(data)
        assert data.flags.c_contiguous
        ptr_data: _ctypes_int_ptr
        if data.dtype == np.int32:
            ptr_data = data.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
            type_data = _C_API_DTYPE_INT32
        elif data.dtype == np.int64:
            ptr_data = data.ctypes.data_as(ctypes.POINTER(ctypes.c_int64))
            type_data = _C_API_DTYPE_INT64
        else:
            raise TypeError(f"Expected np.int32 or np.int64, met type({data.dtype})")
    else:
        raise TypeError(f"Unknown type({type(data).__name__})")
    return (ptr_data, type_data, data)  # return `data` to avoid the temporary copy is freed
