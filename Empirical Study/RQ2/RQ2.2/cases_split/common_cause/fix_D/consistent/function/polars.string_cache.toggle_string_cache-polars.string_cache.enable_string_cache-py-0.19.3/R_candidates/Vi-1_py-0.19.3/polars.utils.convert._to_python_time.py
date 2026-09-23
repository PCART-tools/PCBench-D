def _to_python_time(value: int) -> time:
    """Convert polars int64 (ns) timestamp to python time object."""
    if value == 0:
        return time(microsecond=0)
    else:
        seconds, nanoseconds = divmod(value, 1_000_000_000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return time(
            hour=hours, minute=minutes, second=seconds, microsecond=nanoseconds // 1000
        )
