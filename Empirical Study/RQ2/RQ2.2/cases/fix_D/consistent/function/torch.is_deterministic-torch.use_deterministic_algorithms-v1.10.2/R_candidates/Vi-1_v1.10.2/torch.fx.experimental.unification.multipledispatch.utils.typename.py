def typename(type):
    """Get the name of `type`.
    Parameters
    ----------
    type : Union[Type, Tuple[Type]]
    Returns
    -------
    str
        The name of `type` or a tuple of the names of the types in `type`.
    Examples
    --------
    >>> typename(int)
    'int'
    >>> typename((int, float))
    '(int, float)'
    """
    try:
        return type.__name__
    except AttributeError:
        if len(type) == 1:
            return typename(*type)
        return '(%s)' % ', '.join(map(typename, type))
