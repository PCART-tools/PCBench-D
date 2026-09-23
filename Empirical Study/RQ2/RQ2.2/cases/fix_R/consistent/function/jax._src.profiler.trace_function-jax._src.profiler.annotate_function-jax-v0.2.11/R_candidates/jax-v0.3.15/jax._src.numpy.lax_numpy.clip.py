@_wraps(np.clip, skip_params=['out'])
@jit
def clip(a, a_min=None, a_max=None, out=None):
  _check_arraylike("clip", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.clip is not supported.")
  if a_min is None and a_max is None:
    raise ValueError("At most one of a_min and a_max may be None")
  if a_min is not None:
    a = maximum(a_min, a)
  if a_max is not None:
    a = minimum(a_max, a)
  return a
