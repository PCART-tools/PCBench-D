def dict_to_numpy_array1(d, mapping=None):
    """Convert a dict of numbers to a 1d numpy array with optional mapping.

    .. deprecated:: 2.8

       dict_to_numpy_array1 is deprecated and will be removed in networkx 3.0.
       Use dict_to_numpy_array instead.
    """
    msg = (
        "dict_to_numpy_array1 is deprecated and will be removed in networkx 3.0.\n"
        "Use dict_to_numpy_array instead."
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)

    return _dict_to_numpy_array1(d, mapping)
