def broadcast_to_rank(x: Array, rank: int) -> Array:
  """Adds leading dimensions of ``1`` to give ``x`` rank ``rank``."""
  return broadcast(x, (1,) * (rank - x.ndim))
