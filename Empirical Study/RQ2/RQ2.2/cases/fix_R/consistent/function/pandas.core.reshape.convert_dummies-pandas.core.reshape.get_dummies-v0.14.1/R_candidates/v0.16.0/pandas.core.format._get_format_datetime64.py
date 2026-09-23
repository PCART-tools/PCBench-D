def _get_format_datetime64(is_dates_only, nat_rep='NaT', date_format=None):

    if is_dates_only:
        return lambda x, tz=None: _format_datetime64_dateonly(x,
                                                              nat_rep=nat_rep,
                                                              date_format=date_format)
    else:
        return lambda x, tz=None: _format_datetime64(x, tz=tz, nat_rep=nat_rep)
