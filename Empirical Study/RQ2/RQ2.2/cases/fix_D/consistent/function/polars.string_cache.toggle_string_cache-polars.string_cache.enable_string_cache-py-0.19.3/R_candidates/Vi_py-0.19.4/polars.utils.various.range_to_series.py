def range_to_series(
    name: str, rng: range, dtype: PolarsIntegerType | None = None
) -> Series:
    """Fast conversion of the given range to a Series."""
    dtype = dtype or Int64
    return F.int_range(
        start=rng.start,
        end=rng.stop,
        step=rng.step,
        dtype=dtype,
        eager=True,
    ).alias(name)
