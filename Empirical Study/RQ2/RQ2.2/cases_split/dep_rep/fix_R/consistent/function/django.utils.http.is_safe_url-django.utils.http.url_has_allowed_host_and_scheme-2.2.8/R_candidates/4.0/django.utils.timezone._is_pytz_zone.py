def _is_pytz_zone(tz):
    """Checks if a zone is a pytz zone."""
    # See if pytz was already imported rather than checking
    # settings.USE_DEPRECATED_PYTZ to *allow* manually passing a pytz timezone,
    # which some of the test cases (at least) rely on.
    if not _pytz_imported():
        return False

    # If tz could be pytz, then pytz is needed here.
    import pytz

    _PYTZ_BASE_CLASSES = (pytz.tzinfo.BaseTzInfo, pytz._FixedOffset)
    # In releases prior to 2018.4, pytz.UTC was not a subclass of BaseTzInfo
    if not isinstance(pytz.UTC, pytz._FixedOffset):
        _PYTZ_BASE_CLASSES = _PYTZ_BASE_CLASSES + (type(pytz.UTC),)

    return isinstance(tz, _PYTZ_BASE_CLASSES)
