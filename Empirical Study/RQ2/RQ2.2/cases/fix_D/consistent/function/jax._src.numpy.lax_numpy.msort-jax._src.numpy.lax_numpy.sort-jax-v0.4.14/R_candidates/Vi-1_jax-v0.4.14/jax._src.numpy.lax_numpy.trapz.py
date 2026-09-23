@util._wraps(np.trapz)
@partial(jit, static_argnames=('axis',))
def trapz(y: ArrayLike, x: Optional[ArrayLike] = None, dx: ArrayLike = 1.0, axis: int = -1) -> Array:
  if x is None:
    util.check_arraylike('trapz', y)
    y_arr, = util.promote_dtypes_inexact(y)
  else:
    util.check_arraylike('trapz', y, x)
    y_arr, x_arr = util.promote_dtypes_inexact(y, x)
    if x_arr.ndim == 1:
      dx = diff(x_arr)
    else:
      dx = moveaxis(diff(x_arr, axis=axis), axis, -1)
  y_arr = moveaxis(y_arr, axis, -1)
  return 0.5 * (dx * (y_arr[..., 1:] + y_arr[..., :-1])).sum(-1)
