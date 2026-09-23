def is_string_like(obj):  # from John Hunter, types-free version
    """Check if obj is string.

    .. deprecated:: 2.6
        This is deprecated and will be removed in NetworkX v3.0.
    """
    msg = (
        "is_string_like is deprecated and will be removed in 3.0."
        "Use isinstance(obj, str) instead."
    )
    warnings.warn(msg, DeprecationWarning)
    return isinstance(obj, str)
