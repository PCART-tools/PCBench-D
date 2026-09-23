def is_type_factory(_type):
    """

    Parameters
    ----------
    `_type` - a type to be compared against (e.g. type(x) == `_type`)

    Returns
    -------
    validator - a function of a single argument x , which returns the
                True if type(x) is equal to `_type`

    """

    def inner(x):
        if type(x) != _type:
            raise ValueError("Value must have type '%s'" % str(_type))

    return inner
