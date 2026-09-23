def _get_rc_timezone():
    """Retrieve the preferred timezone from the rcParams dictionary."""
    s = mpl.rcParams['timezone']
    if s == 'UTC':
        return UTC
    return dateutil.tz.gettz(s)
