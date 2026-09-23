def _canonicalize_dimension(dim: DimSize) -> DimSize:
  if isinstance(dim, Tracer) and config.jax_dynamic_shapes:
    return dim
  elif (config.jax_dynamic_shapes and isinstance(dim, DArray) and
        type(dim._aval.dtype) is bint and not dim._aval.shape):
    return dim
  elif is_special_dim_size(dim):
    return dim
  else:
    return operator.index(dim)
