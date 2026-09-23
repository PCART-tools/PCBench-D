def is_numpy_column_array(data):
    """Check whether data is a column numpy array."""
    if not isinstance(data, np.ndarray):
        return False
    shape = data.shape
    return len(shape) == 2 and shape[1] == 1
