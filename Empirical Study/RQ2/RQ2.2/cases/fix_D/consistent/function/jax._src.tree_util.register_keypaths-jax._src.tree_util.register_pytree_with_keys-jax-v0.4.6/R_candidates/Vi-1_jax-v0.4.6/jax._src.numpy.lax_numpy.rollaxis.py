@util._wraps(np.rollaxis, lax_description=_ARRAY_VIEW_DOC)
@partial(jit, static_argnames=('axis', 'start'))
def rollaxis(a, axis: int, start=0):
  util._check_arraylike("rollaxis", a)
  start = core.concrete_or_error(operator.index, start, "'start' argument of jnp.rollaxis()")
  a_ndim = ndim(a)
  axis = _canonicalize_axis(axis, a_ndim)
  if not (-a_ndim <= start <= a_ndim):
    raise ValueError(f"{start=} must satisfy {-a_ndim}<=start<={a_ndim}")
  if start < 0:
    start += a_ndim
  if start > axis:
    start -= 1
  return moveaxis(a, axis, start)
