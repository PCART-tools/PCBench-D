def c_float_array(data):
    """Get pointer of float numpy array / list."""
    if is_1d_list(data):
        data = np.array(data, copy=False)
    if is_numpy_1d_array(data):
        data = convert_from_sliced_object(data)
        assert data.flags.c_contiguous
        if data.dtype == np.float32:
            ptr_data = data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            type_data = C_API_DTYPE_FLOAT32
        elif data.dtype == np.float64:
            ptr_data = data.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
            type_data = C_API_DTYPE_FLOAT64
        else:
            raise TypeError(f"Expected np.float32 or np.float64, met type({data.dtype})")
    else:
        raise TypeError(f"Unknown type({type(data).__name__})")
    return (ptr_data, type_data, data)  # return `data` to avoid the temporary copy is freed
