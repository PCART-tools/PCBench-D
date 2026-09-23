def _prepare_other_arg(other: Any, length: int | None = None) -> Series:
    # if not a series create singleton series such that it will broadcast
    value = other
    if not isinstance(other, pl.Series):
        if isinstance(other, str):
            pass
        elif isinstance(other, Sequence):
            raise TypeError("operation not supported")
        other = pl.Series("", [other])

    if length and length > 1:
        other = other.extend_constant(value=value, n=length - 1)

    return other
