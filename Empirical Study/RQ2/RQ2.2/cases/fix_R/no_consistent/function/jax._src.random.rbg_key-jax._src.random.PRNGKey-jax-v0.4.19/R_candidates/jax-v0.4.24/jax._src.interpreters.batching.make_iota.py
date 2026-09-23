def make_iota(axis_size: AxisSize) -> Array:
  handler = make_iota_handlers.get(type(axis_size))
  if handler:
    return handler(axis_size)
  else:
    return jax.lax.iota('int32', int(axis_size))
