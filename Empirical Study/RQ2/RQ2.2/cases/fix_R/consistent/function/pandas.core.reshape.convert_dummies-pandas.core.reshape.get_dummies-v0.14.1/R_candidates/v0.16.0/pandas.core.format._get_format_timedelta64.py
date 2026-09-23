def _get_format_timedelta64(values, nat_rep='NaT', box=False):
    """
    Return a formatter function for a range of timedeltas.
    These will all have the same format argument

    If box, then show the return in quotes
    """

    values_int = values.astype(np.int64)

    consider_values = values_int != iNaT

    one_day_nanos = (86400 * 1e9)
    even_days = np.logical_and(consider_values, values_int % one_day_nanos != 0).sum() == 0
    all_sub_day = np.logical_and(consider_values, np.abs(values_int) >= one_day_nanos).sum() == 0

    if even_days:
        format = 'even_day'
    elif all_sub_day:
        format = 'sub_day'
    else:
        format = 'long'

    def _formatter(x):
        if x is None or lib.checknull(x):
            return nat_rep

        if not isinstance(x, Timedelta):
            x = Timedelta(x)
        result = x._repr_base(format=format)
        if box:
            result = "'{0}'".format(result)
        return result

    return _formatter
