@_wraps(np.trapz)
@partial(jit, static_argnames=('axis',))
def trapz(y, x=None, dx=1.0, axis: int = -1):
  if x is None:
    _check_arraylike('trapz', y)
    y, = _promote_dtypes_inexact(y)
  else:
    _check_arraylike('trapz', y, x)
    y, x = _promote_dtypes_inexact(y, x)
    if ndim(x) == 1:
      dx = diff(x)
    else:
      dx = moveaxis(diff(x, axis=axis), axis, -1)
  y = moveaxis(y, axis, -1)
  return 0.5 * (dx * (y[..., 1:] + y[..., :-1])).sum(-1)
