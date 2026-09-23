def _jax_type(dtype, weak_type):
  """Return the jax type for a dtype and weak type."""
  if weak_type:
    if dtype == bool:
      return dtype
    if dtype == _bfloat16_dtype:
      return float
    return type(dtype.type(0).item())
  return dtype
