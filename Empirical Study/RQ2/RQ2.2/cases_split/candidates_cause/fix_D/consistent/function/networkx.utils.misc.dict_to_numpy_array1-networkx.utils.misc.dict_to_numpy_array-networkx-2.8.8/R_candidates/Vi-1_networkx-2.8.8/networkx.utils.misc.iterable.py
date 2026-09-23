def iterable(obj):
    """Return True if obj is iterable with a well-defined len().

    .. deprecated:: 2.6
        This is deprecated and will be removed in NetworkX v3.0.
    """
    msg = (
        "iterable is deprecated and will be removed in 3.0."
        "Use isinstance(obj, (collections.abc.Iterable, collections.abc.Sized)) instead."
    )
    warnings.warn(msg, DeprecationWarning)
    if hasattr(obj, "__iter__"):
        return True
    try:
        len(obj)
    except:
        return False
    return True
