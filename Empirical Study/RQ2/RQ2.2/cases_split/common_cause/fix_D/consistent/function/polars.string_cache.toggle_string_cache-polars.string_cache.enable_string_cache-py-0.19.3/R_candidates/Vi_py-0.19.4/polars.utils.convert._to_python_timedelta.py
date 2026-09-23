def _to_python_timedelta(value: int | float, time_unit: TimeUnit = "ns") -> timedelta:
    if time_unit == "ns":
        return timedelta(microseconds=value // 1e3)
    elif time_unit == "us":
        return timedelta(microseconds=value)
    elif time_unit == "ms":
        return timedelta(milliseconds=value)
    else:
        raise ValueError(
            f"time_unit must be one of {{'ns', 'us', 'ms'}}, got {time_unit!r}"
        )
