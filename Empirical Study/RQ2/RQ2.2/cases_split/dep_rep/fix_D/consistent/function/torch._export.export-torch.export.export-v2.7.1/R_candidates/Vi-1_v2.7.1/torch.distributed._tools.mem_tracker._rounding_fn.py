def _rounding_fn(value: int, divisor: int, precision: int) -> Union[float, int]:
    return value if divisor == 1 else round(value / divisor, precision)
