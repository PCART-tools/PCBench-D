def _get_special_dim_handler(dim: DimSize) -> Optional[DimensionHandler]:
  if isinstance(dim, Tracer) and not config.jax_dynamic_shapes:
    return None
  if isinstance(dim, DArray) and not dim.shape and type(dim.dtype) is bint:
    return DArrayDimHandler
  return _SPECIAL_DIMENSION_HANDLERS.get(type(dim))
