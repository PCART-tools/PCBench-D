def wrap_ldf(ldf: PyLazyFrame) -> LazyFrame:
    return pl.LazyFrame._from_pyldf(ldf)
