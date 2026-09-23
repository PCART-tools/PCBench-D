def _prod(xs: Iterable[int]) -> int:
    """Compute product of a list"""
    prod = 1
    for x in xs:
        prod *= x
    return prod
