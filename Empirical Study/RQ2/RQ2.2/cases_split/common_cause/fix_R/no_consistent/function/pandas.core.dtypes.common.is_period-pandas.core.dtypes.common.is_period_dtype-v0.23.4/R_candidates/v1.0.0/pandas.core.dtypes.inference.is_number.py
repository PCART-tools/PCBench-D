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
    is_number : bool
        Whether `obj` is a number or not.

    See Also
    --------
    api.types.is_integer: Checks a subgroup of numbers.

    Examples
    --------
    >>> pd.api.types.is_number(1)
    True
    >>> pd.api.types.is_number(7.15)
    True

    Booleans are valid because they are int subclass.

    >>> pd.api.types.is_number(False)
    True

    >>> pd.api.types.is_number("foo")
    False
    >>> pd.api.types.is_number("5")
    False
    """

    return isinstance(obj, (Number, np.number))
