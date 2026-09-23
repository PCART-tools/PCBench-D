def top_k(operand: Array, k: int) -> Tuple[Array, Array]:
  """Returns top ``k`` values and their indices along the last axis of ``operand``."""
  k = int(k)
  if k < 0:
    raise ValueError(f"k argument to top_k must be nonnegative, got {k}")
  return top_k_p.bind(operand, k=k)
