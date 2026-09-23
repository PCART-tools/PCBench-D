def _is_dates_only(values):
    # return a boolean if we are only dates (and don't have a timezone)
    from pandas import DatetimeIndex
    values = DatetimeIndex(values)
    if values.tz is not None:
        return False

    values_int = values.asi8
    consider_values = values_int != iNaT
    one_day_nanos = (86400 * 1e9)
    even_days = np.logical_and(consider_values, values_int % one_day_nanos != 0).sum() == 0
    if even_days:
        return True
    return False
