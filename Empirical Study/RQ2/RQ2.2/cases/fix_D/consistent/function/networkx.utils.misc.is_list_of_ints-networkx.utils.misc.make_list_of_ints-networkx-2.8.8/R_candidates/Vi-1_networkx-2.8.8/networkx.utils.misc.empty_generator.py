def empty_generator():
    """Return a generator with no members.

    .. deprecated:: 2.6
    """
    warnings.warn(
        "empty_generator is deprecated and will be removed in v3.0.", DeprecationWarning
    )
    return (i for i in ())
