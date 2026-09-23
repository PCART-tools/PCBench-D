def is_iterator(obj):
    """Returns True if and only if the given object is an iterator object.

    .. deprecated:: 2.6.0
        Deprecated in favor of ``isinstance(obj, collections.abc.Iterator)``
    """
    msg = (
        "is_iterator is deprecated and will be removed in version 3.0. "
        "Use ``isinstance(obj, collections.abc.Iterator)`` instead."
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)
    has_next_attr = hasattr(obj, "__next__") or hasattr(obj, "next")
    return iter(obj) is obj and has_next_attr
