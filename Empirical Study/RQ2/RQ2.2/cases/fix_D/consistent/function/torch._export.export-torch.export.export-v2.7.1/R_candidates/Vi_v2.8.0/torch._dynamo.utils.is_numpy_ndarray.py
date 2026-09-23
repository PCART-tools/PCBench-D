def is_numpy_ndarray(value):
    if not np:
        return False

    return istype(value, np.ndarray)
