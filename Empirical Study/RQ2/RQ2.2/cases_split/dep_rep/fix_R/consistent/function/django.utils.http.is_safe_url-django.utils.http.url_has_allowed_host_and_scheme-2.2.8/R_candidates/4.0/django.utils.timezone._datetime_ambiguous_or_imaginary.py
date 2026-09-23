def _datetime_ambiguous_or_imaginary(dt, tz):
    if _is_pytz_zone(tz):
        import pytz
        try:
            tz.utcoffset(dt)
        except (pytz.AmbiguousTimeError, pytz.NonExistentTimeError):
            return True
        else:
            return False

    return tz.utcoffset(dt.replace(fold=not dt.fold)) != tz.utcoffset(dt)
