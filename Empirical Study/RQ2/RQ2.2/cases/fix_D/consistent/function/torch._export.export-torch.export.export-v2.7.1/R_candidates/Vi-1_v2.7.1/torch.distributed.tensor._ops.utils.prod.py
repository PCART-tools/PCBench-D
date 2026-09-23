def prod(xs: Iterable[int]) -> int:
    return functools.reduce(operator.mul, xs, 1)
