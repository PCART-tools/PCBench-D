def cumprod(operand: Array, axis: int = 0, reverse: bool = False) -> Array:
  """Computes a cumulative product along `axis`."""
  return cumprod_p.bind(operand, axis=int(axis), reverse=bool(reverse))
