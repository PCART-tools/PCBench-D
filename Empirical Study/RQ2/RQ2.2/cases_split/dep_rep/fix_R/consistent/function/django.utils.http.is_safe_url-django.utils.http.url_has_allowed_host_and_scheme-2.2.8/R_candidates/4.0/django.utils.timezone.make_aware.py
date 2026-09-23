def make_aware(value, timezone=None, is_dst=NOT_PASSED):
    """Make a naive datetime.datetime in a given time zone aware."""
    if is_dst is NOT_PASSED:
        is_dst = None
    else:
        warnings.warn(
            'The is_dst argument to make_aware(), used by the Trunc() '
            'database functions and QuerySet.datetimes(), is deprecated as it '
            'has no effect with zoneinfo time zones.',
            RemovedInDjango50Warning,
        )
    if timezone is None:
        timezone = get_current_timezone()
    if _is_pytz_zone(timezone):
        # This method is available for pytz time zones.
        return timezone.localize(value, is_dst=is_dst)
    else:
        # Check that we won't overwrite the timezone of an aware datetime.
        if is_aware(value):
            raise ValueError(
                "make_aware expects a naive datetime, got %s" % value)
        # This may be wrong around DST changes!
        return value.replace(tzinfo=timezone)
