def _is_numpy_2d_array(data: Any) -> bool:
    """Check whether data is a numpy 2-D array."""
    return isinstance(data, np.ndarray) and len(data.shape) == 2 and data.shape[1] > 1
