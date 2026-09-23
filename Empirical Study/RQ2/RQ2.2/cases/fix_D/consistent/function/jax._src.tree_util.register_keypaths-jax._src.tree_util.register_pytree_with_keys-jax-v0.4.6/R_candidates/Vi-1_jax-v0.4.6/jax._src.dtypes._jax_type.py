def _jax_type(dtype: DType, weak_type: bool) -> JAXType:
  """Return the jax type for a dtype and weak type."""
  if weak_type:
    if dtype == bool:
      return dtype
    if _fp8_enabled and dtype in [_float8_e4m3fn_dtype, _float8_e5m2_dtype]:
      return float
    if dtype == _bfloat16_dtype:
      return float
    return type(dtype.type(0).item())
  return dtype
