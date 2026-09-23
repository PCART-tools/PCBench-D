@_wraps(np.unwrap)
@partial(jit, static_argnames=('axis',))
def unwrap(p, discont=None, axis: int = -1, period = 2 * pi):
  _check_arraylike("unwrap", p)
  p = asarray(p)
  if issubdtype(p.dtype, np.complexfloating):
    raise ValueError("jnp.unwrap does not support complex inputs.")
  if p.shape[axis] == 0:
    return _promote_dtypes_inexact(p)[0]
  if discont is None:
    discont = period / 2
  interval = period / 2
  dd = diff(p, axis=axis)
  ddmod = mod(dd + interval, period) - interval
  ddmod = where((ddmod == -interval) & (dd > 0), interval, ddmod)

  ph_correct = where(abs(dd) < discont, 0, ddmod - dd)

  up = concatenate((
    lax.slice_in_dim(p, 0, 1, axis=axis),
    lax.slice_in_dim(p, 1, None, axis=axis) + cumsum(ph_correct, axis=axis)
  ), axis=axis)

  return up
