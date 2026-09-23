def _get_format_datetime64_from_values(values,
                                       nat_rep='NaT',
                                       date_format=None):
    is_dates_only = _is_dates_only(values)
    return _get_format_datetime64(is_dates_only=is_dates_only,
                                  nat_rep=nat_rep,
                                  date_format=date_format)
