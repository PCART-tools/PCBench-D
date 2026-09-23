def activate(timezone):
    """
    Set the time zone for the current thread.

    The ``timezone`` argument must be an instance of a tzinfo subclass or a
    time zone name.
    """
    if isinstance(timezone, tzinfo):
        _active.value = timezone
    elif isinstance(timezone, str):
        if settings.USE_DEPRECATED_PYTZ:
            import pytz
            _active.value = pytz.timezone(timezone)
        else:
            _active.value = zoneinfo.ZoneInfo(timezone)
    else:
        raise ValueError("Invalid timezone: %r" % timezone)
