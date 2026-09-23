def cummin(operand: Array, axis: int = 0, reverse: bool = False) -> Array:
  """Computes a cumulative minimum along `axis`."""
  return cummin_p.bind(operand, axis=int(axis), reverse=bool(reverse))
