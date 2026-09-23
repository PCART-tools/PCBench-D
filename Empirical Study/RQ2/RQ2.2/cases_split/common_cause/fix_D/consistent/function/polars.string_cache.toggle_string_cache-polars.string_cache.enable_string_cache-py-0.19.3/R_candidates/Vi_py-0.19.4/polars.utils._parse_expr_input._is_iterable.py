def _is_iterable(input: IntoExpr | Iterable[IntoExpr]) -> bool:
    return isinstance(input, Iterable) and not isinstance(
        input, (str, bytes, pl.Series)
    )
