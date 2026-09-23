def _format_datetime64_dateonly(x, nat_rep='NaT', date_format=None):
    if x is None or lib.checknull(x):
        return nat_rep

    if not isinstance(x, Timestamp):
        x = Timestamp(x)

    if date_format:
        return x.strftime(date_format)
    else:
        return x._date_repr
