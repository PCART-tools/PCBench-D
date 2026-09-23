def is_re(obj) -> bool:
    """
    Check if the object is a regex pattern instance.

    Parameters
    ----------
    obj : The object to check

    Returns
    -------
    is_regex : bool
        Whether `obj` is a regex pattern.

    Examples
    --------
    >>> is_re(re.compile(".*"))
    True
    >>> is_re("foo")
    False
    """
    return isinstance(obj, Pattern)
