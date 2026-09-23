def _make_sliced_dtype_np_lt_14(dtype, index):
    # For numpy < 1.14
    dt = np.dtype([(name, dtype[name]) for name in index])
    return dt
