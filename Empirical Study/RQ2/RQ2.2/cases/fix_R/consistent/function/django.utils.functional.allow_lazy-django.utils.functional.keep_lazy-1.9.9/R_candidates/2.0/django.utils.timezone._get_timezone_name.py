def _get_timezone_name(timezone):
    """Return the name of ``timezone``."""
    try:
        # for pytz timezones
        return timezone.zone
    except AttributeError:
        # for regular tzinfo objects
        return timezone.tzname(None)
