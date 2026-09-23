def is_datetimetz(arr):
    """
    Check whether an array-like is a datetime array-like with a timezone
    component in its dtype.

    Parameters
    ----------
    arr : array-like
        The array-like to check.

    Returns
    -------
    boolean : Whether or not the array-like is a datetime array-like with
              a timezone component in its dtype.

    Examples
    --------
    >>> is_datetimetz([1, 2, 3])
    False

    Although the following examples are both DatetimeIndex objects,
    the first one returns False because it has no timezone component
    unlike the second one, which returns True.

    >>> is_datetimetz(pd.DatetimeIndex([1, 2, 3]))
    False
    >>> is_datetimetz(pd.DatetimeIndex([1, 2, 3], tz="US/Eastern"))
    True

    The object need not be a DatetimeIndex object. It just needs to have
    a dtype which has a timezone component.

    >>> dtype = DatetimeTZDtype("ns", tz="US/Eastern")
    >>> s = pd.Series([], dtype=dtype)
    >>> is_datetimetz(s)
    True
    """

    # TODO: do we need this function?
    # It seems like a repeat of is_datetime64tz_dtype.

    return ((isinstance(arr, ABCDatetimeIndex) and
             getattr(arr, 'tz', None) is not None) or
            is_datetime64tz_dtype(arr))
