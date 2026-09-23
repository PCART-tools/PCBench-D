def _coerce_to_dtype(dtype):
    """ coerce a string / np.dtype to a dtype """
    if is_categorical_dtype(dtype):
        dtype = CategoricalDtype()
    else:
        dtype = np.dtype(dtype)
    return dtype
