def ensure_python_int(value: Union[int, np.integer]) -> int:
    """
    Ensure that a value is a python int.

    Parameters
    ----------
    value: int or numpy.integer

    Returns
    -------
    int

    Raises
    ------
    TypeError: if the value isn't an int or can't be converted to one.
    """
    if not is_scalar(value):
        raise TypeError(f"Value needs to be a scalar value, was type {type(value)}")
    msg = "Wrong type {} for value {}"
    try:
        new_value = int(value)
        assert new_value == value
    except (TypeError, ValueError, AssertionError):
        raise TypeError(msg.format(type(value), value))
    return new_value
