def is_array_scalar(x):
    """Test whether `x` is either a scalar or an array scalar.

    """
    return np.size(x) == 1
