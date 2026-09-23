def is_datetimelike_v_numeric(a, b):
    """
    Check if we are comparing a datetime-like object to a numeric object.
    By "numeric," we mean an object that is either of an int or float dtype.

    Parameters
    ----------
    a : array-like, scalar
        The first object to check.
    b : array-like, scalar
        The second object to check.

    Returns
    -------
    boolean
        Whether we return a comparing a datetime-like to a numeric object.

    Examples
    --------
    >>> dt = np.datetime64(pd.datetime(2017, 1, 1))
    >>>
    >>> is_datetimelike_v_numeric(1, 1)
    False
    >>> is_datetimelike_v_numeric(dt, dt)
    False
    >>> is_datetimelike_v_numeric(1, dt)
    True
    >>> is_datetimelike_v_numeric(dt, 1)  # symmetric check
    True
    >>> is_datetimelike_v_numeric(np.array([dt]), 1)
    True
    >>> is_datetimelike_v_numeric(np.array([1]), dt)
    True
    >>> is_datetimelike_v_numeric(np.array([dt]), np.array([1]))
    True
    >>> is_datetimelike_v_numeric(np.array([1]), np.array([2]))
    False
    >>> is_datetimelike_v_numeric(np.array([dt]), np.array([dt]))
    False
    """

    if not hasattr(a, "dtype"):
        a = np.asarray(a)
    if not hasattr(b, "dtype"):
        b = np.asarray(b)

    def is_numeric(x):
        """
        Check if an object has a numeric dtype (i.e. integer or float).
        """
        return is_integer_dtype(x) or is_float_dtype(x)

    return (needs_i8_conversion(a) and is_numeric(b)) or (
        needs_i8_conversion(b) and is_numeric(a)
    )
