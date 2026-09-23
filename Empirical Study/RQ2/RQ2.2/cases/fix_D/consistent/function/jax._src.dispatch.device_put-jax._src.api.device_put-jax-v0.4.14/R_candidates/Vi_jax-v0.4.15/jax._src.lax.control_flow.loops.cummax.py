def cummax(operand: Array, axis: int = 0, reverse: bool = False) -> Array:
  """Computes a cumulative maximum along `axis`."""
  return cummax_p.bind(operand, axis=int(axis), reverse=bool(reverse))
