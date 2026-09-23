def _make_sliced_dtype(dtype, index):
    if LooseVersion(np.__version__) == LooseVersion("1.14.0"):
        return _make_sliced_dtype_np_ge_14(dtype, index)
    else:
        return _make_sliced_dtype_np_lt_14(dtype, index)
