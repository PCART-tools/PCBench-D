def series_to_pyseries(name: str, values: Series) -> PySeries:
    """Construct a new PySeries from a Polars Series."""
    py_s = values._s.clone()
    py_s.rename(name)
    return py_s
