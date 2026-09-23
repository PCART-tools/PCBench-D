def _view_if_needed(values):
    if is_datetime_or_timedelta_dtype(values):
        return values.view(np.int64)
    return values
