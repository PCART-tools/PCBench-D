def _maybe_box_datetimelike(value):
    # turn a datetime like into a Timestamp/timedelta as needed

    if isinstance(value, (np.datetime64, datetime)):
        value = tslib.Timestamp(value)
    elif isinstance(value, (np.timedelta64, timedelta)):
        value = tslib.Timedelta(value)

    return value
