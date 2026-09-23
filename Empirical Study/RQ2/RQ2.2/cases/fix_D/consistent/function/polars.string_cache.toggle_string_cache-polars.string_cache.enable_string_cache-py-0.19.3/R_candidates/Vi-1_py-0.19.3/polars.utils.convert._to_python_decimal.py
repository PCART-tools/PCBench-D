def _to_python_decimal(
    sign: int, digits: Sequence[int], prec: int, scale: int
) -> Decimal:
    return _create_decimal_with_prec(prec)((sign, digits, scale))
