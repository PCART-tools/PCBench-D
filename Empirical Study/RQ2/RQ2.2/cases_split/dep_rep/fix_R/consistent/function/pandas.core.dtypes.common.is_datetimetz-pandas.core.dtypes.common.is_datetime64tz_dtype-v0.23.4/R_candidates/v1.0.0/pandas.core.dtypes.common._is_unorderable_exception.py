def _is_unorderable_exception(e: TypeError) -> bool:
    """
    Check if the exception raised is an unorderable exception.

    Parameters
    ----------
    e : Exception or sub-class
        The exception object to check.

    Returns
    -------
    bool
        Whether or not the exception raised is an unorderable exception.
    """
    return "'>' not supported between instances of" in str(e)
