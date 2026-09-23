def is_number(obj) -> bool:
    """
    Check if the object is a number.

    Returns True when the object is a number, and False if is not.

    Parameters
    ----------
    obj : any type
        The object to check if is a number.

    Returns
    -------
    bool
        Whether `obj` is a number or not.

    See Also
    --------
    api.types.is_integer: Checks a subgroup of numbers.

    Examples
    --------
    >>> from pandas.api.types import is_number
    >>> is_number(1)
    True
    >>> is_number(7.15)
    True

    Booleans are valid because they are int subclass.

    >>> is_number(False)
    True

    >>> is_number("foo")
    False
    >>> is_number("5")
    False
    """
    return isinstance(obj, (Number, np.number))
