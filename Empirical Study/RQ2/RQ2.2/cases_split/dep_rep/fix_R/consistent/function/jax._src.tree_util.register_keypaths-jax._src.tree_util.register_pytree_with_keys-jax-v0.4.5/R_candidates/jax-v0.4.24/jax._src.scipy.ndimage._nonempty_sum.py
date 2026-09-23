def _nonempty_sum(arrs: Sequence[Array]) -> Array:
  return functools.reduce(operator.add, arrs)
