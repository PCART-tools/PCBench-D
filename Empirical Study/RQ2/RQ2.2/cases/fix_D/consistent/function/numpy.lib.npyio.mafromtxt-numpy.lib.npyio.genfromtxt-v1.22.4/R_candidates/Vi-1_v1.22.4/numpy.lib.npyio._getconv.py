def _getconv(dtype):
    """
    Find the correct dtype converter. Adapted from matplotlib.

    Even when a lambda is returned, it is defined at the toplevel, to allow
    testing for equality and enabling optimization for single-type data.
    """
    for base, conv in _CONVERTERS:
        if issubclass(dtype.type, base):
            return conv
    return str
