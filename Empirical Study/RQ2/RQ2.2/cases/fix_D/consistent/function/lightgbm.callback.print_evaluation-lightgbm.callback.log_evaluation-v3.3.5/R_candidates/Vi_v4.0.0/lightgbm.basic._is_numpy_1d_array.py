def _is_numpy_1d_array(data: Any) -> bool:
    """Check whether data is a numpy 1-D array."""
    return isinstance(data, np.ndarray) and len(data.shape) == 1
