def _timedelta_to_pl_timedelta(td: timedelta, time_unit: TimeUnit | None = None) -> int:
    if time_unit == "ns":
        return int(td.total_seconds() * 1e9)
    elif time_unit == "us":
        return int(td.total_seconds() * 1e6)
    elif time_unit == "ms":
        return int(td.total_seconds() * 1e3)
    elif time_unit is None:
        # python has us precision
        return int(td.total_seconds() * 1e6)
    else:
        raise ValueError(
            f"time_unit must be one of {{'ns', 'us', 'ms'}}, got {time_unit!r}"
        )
