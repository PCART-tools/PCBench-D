def _make_sliced_dtype_np_ge_14(dtype, index):
    # For https://github.com/numpy/numpy/pull/6053, NumPy >= 1.14
    new = {
        'names': index,
        'formats': [dtype.fields[name][0] for name in index],
        'offsets': [dtype.fields[name][1] for name in index],
        'itemsize': dtype.itemsize,
    }
    return np.dtype(new)
