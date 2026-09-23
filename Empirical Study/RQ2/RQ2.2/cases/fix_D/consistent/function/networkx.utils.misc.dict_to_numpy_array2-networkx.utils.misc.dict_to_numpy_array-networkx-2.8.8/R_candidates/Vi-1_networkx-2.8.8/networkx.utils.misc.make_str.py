def make_str(x):
    """Returns the string representation of t.

    .. deprecated:: 2.6
        This is deprecated and will be removed in NetworkX v3.0.
    """
    msg = "make_str is deprecated and will be removed in 3.0. Use str instead."
    warnings.warn(msg, DeprecationWarning)
    return str(x)
