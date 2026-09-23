class DatetimeAccessor(Accessor):
    """ Accessor object for datetimelike properties of the Series values.

    Examples
    --------

    >>> s.dt.microsecond  # doctest: +SKIP
    """
    _accessor = pd.Series.dt
    _accessor_name = 'dt'
