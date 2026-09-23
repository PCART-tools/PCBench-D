def iterable_to_pyseries(
    name: str,
    values: Iterable[Any],
    dtype: PolarsDataType | None = None,
    *,
    dtype_if_empty: PolarsDataType | None = None,
    chunk_size: int = 1_000_000,
    strict: bool = True,
) -> PySeries:
    """Construct a PySeries from an iterable/generator."""
    if not isinstance(values, (Generator, Iterator)):
        values = iter(values)

    def to_series_chunk(values: list[Any], dtype: PolarsDataType | None) -> Series:
        return pl.Series(
            name=name,
            values=values,
            dtype=dtype,
            strict=strict,
            dtype_if_empty=dtype_if_empty,
        )

    n_chunks = 0
    series: Series = None  # type: ignore[assignment]
    while True:
        slice_values = list(islice(values, chunk_size))
        if not slice_values:
            break
        schunk = to_series_chunk(slice_values, dtype)
        if series is None:
            series = schunk
            dtype = series.dtype
        else:
            series.append(schunk)
            n_chunks += 1

    if series is None:
        series = to_series_chunk([], dtype)
    if n_chunks > 0:
        series.rechunk(in_place=True)

    return series._s
