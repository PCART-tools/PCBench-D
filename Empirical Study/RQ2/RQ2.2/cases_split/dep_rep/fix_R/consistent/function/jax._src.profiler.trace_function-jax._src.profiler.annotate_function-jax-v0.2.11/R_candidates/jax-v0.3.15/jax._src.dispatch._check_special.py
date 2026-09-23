def _check_special(name, xla_shape, buf):
  assert not xla_shape.is_tuple()
  if dtypes.issubdtype(xla_shape.element_type(), np.inexact):
    if config.jax_debug_nans and np.any(np.isnan(buf.to_py())):
      raise FloatingPointError(f"invalid value (nan) encountered in {name}")
    if config.jax_debug_infs and np.any(np.isinf(buf.to_py())):
      raise FloatingPointError(f"invalid value (inf) encountered in {name}")
