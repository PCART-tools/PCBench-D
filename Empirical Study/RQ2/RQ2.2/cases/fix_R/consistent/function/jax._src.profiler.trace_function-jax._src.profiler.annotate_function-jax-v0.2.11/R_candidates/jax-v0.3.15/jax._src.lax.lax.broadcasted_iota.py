def broadcasted_iota(dtype: DType, shape: Shape, dimension: int) -> Array:
  """Convenience wrapper around ``iota``."""
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = canonicalize_shape(shape)
  dynamic_shape = [d for d in shape if isinstance(d, core.Tracer)]
  static_shape = [None if isinstance(d, core.Tracer) else d for d in shape]
  dimension = core.concrete_or_error(
      int, dimension, "dimension argument of lax.broadcasted_iota")
  return iota_p.bind(*dynamic_shape, dtype=dtype, shape=tuple(static_shape),
                     dimension=dimension)
