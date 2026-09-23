def _format_datetime64(x, tz=None, nat_rep='NaT'):
    if x is None or lib.checknull(x):
        return nat_rep

    if tz is not None or not isinstance(x, Timestamp):
        x = Timestamp(x, tz=tz)

    return str(x)
