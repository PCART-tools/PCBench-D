def is_callable(obj):
    """

    Parameters
    ----------
    `obj` - the object to be checked

    Returns
    -------
    validator - returns True if object is callable
        raises ValueError otherwise.

    """
    if not callable(obj):
        raise ValueError("Value must be a callable")
    return True
