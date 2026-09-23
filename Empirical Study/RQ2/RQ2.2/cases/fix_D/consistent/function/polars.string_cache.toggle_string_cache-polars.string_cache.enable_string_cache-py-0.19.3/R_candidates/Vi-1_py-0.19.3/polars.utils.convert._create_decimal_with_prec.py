@lru_cache(None)
def _create_decimal_with_prec(
    precision: int,
) -> Callable[[tuple[int, Sequence[int], int]], Decimal]:
    # pre-cache contexts so we don't have to spend time on recreating them every time
    return Context(prec=precision).create_decimal
