def _localize(dt: datetime, time_zone: str) -> datetime:
    # zone info installation should already be checked
    _tzinfo: ZoneInfo | tzinfo
    try:
        _tzinfo = get_zoneinfo(time_zone)
    except zoneinfo.ZoneInfoNotFoundError:
        # try fixed offset, which is not supported by ZoneInfo
        _tzinfo = _parse_fixed_tz_offset(time_zone)

    return dt.astimezone(_tzinfo)
