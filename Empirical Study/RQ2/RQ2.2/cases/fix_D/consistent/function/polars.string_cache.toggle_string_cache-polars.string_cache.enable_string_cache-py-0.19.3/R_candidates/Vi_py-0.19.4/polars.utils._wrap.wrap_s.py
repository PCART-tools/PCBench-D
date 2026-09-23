def wrap_s(s: PySeries) -> Series:
    return pl.Series._from_pyseries(s)
