def _canonicalize_dimension(dim: DimSize) -> DimSize:
  # Dimensions are most commonly integral (by far), so we check that first.
  try:
    return operator.index(dim)
  except TypeError as e:
    type_error = e
  if isinstance(dim, Tracer) and config.jax_dynamic_shapes:
    return dim
  elif (config.jax_dynamic_shapes and isinstance(dim, DArray) and
        type(dim._aval.dtype) is bint and not dim._aval.shape):
    return dim
  elif is_special_dim_size(dim):
    return dim
  else:
    raise type_error
