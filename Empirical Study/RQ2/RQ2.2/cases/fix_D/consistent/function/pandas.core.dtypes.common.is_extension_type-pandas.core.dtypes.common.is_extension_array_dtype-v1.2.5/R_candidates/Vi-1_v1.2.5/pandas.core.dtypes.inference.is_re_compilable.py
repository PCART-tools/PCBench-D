def is_re_compilable(obj) -> bool:
    """
    Check if the object can be compiled into a regex pattern instance.

    Parameters
    ----------
    obj : The object to check

    Returns
    -------
    is_regex_compilable : bool
        Whether `obj` can be compiled as a regex pattern.

    Examples
    --------
    >>> is_re_compilable(".*")
    True
    >>> is_re_compilable(1)
    False
    """
    try:
        re.compile(obj)
    except TypeError:
        return False
    else:
        return True
