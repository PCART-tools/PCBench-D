def _prepare_rolling_window_args(
    window_size: int | timedelta | str,
    min_periods: int | None = None,
) -> tuple[str, int]:
    if isinstance(window_size, int):
        if window_size < 1:
            raise ValueError("`window_size` must be positive")

        if min_periods is None:
            min_periods = window_size
        window_size = f"{window_size}i"
    elif isinstance(window_size, timedelta):
        window_size = _timedelta_to_pl_duration(window_size)
    if min_periods is None:
        min_periods = 1
    return window_size, min_periods
