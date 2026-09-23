def non_negative_dim(d: DimSize) -> DimSize:
  """max(d, 0)."""
  if is_constant_dim(d):
    return max(0, d)
  assert is_symbolic_dim(d)
  try:
    d_ge_0 = (d >= 0)
    return d if d_ge_0 else 0
  except InconclusiveDimensionOperation:
    return d.non_negative()  # type: ignore
