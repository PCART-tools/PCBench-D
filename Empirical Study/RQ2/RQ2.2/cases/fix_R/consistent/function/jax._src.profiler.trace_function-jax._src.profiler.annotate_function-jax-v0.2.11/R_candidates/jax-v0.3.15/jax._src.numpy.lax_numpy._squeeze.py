@partial(jit, static_argnames=('axis',), inline=True)
def _squeeze(a, axis):
  _check_arraylike("squeeze", a)
  if axis is None:
    a_shape = shape(a)
    axis = tuple(i for i, d in enumerate(a_shape) if d == 1)
  return lax.squeeze(a, axis)
