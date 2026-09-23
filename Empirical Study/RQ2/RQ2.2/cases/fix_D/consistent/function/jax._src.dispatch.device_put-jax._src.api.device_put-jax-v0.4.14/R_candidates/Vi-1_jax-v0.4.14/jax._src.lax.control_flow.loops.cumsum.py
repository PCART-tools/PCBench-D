def cumsum(operand: Array, axis: int = 0, reverse: bool = False) -> Array:
  """Computes a cumulative sum along `axis`."""
  return cumsum_p.bind(operand, axis=int(axis), reverse=bool(reverse))
