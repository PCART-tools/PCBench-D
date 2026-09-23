def scalar_type_of(x: Any) -> type:
  """Return the scalar type associated with a JAX value."""
  typ = dtype(x)
  if typ == bfloat16:
    return float
  elif _fp8_enabled and typ == float8_e4m3fn:
    return float
  elif _fp8_enabled and typ == float8_e5m2:
    return float
  elif np.issubdtype(typ, np.bool_):
    return bool
  elif np.issubdtype(typ, np.integer):
    return int
  elif np.issubdtype(typ, np.floating):
    return float
  elif np.issubdtype(typ, np.complexfloating):
    return complex
  else:
    raise TypeError(f"Invalid scalar value {x}")
