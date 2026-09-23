def ensure_float(arr):
    if issubclass(arr.dtype.type, (np.integer, np.bool_)):
        arr = arr.astype(float)
    return arr
