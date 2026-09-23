def convert_from_sliced_object(data):
    """Fix the memory of multi-dimensional sliced object."""
    if isinstance(data, np.ndarray) and isinstance(data.base, np.ndarray):
        if not data.flags.c_contiguous:
            _log_warning("Usage of np.ndarray subset (sliced data) is not recommended "
                         "due to it will double the peak memory cost in LightGBM.")
            return np.copy(data)
    return data
