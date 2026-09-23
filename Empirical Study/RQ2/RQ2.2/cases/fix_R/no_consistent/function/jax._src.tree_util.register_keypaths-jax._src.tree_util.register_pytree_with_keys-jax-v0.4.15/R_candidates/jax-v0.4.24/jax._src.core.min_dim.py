def min_dim(d1: DimSize, d2: DimSize) -> DimSize:
  """Like min(d1, d2) but for both constant and symbolic dimensions."""
  d1_is_constant = is_constant_dim(d1)
  if d1_is_constant and is_constant_dim(d2):
    return min(d1, d2)
  if d1_is_constant:
    return d2.rmin(d1)  # type: ignore[union-attr]
  else:
    return d1.min(d2)  # type: ignore[union-attr]
