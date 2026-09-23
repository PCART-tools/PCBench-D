@util._wraps(np.interp)
@jit
def interp(x: ArrayLike, xp: ArrayLike, fp: ArrayLike,
           left: Optional[ArrayLike] = None,
           right: Optional[ArrayLike] = None,
           period: Optional[ArrayLike] = None) -> Array:
  util._check_arraylike("interp", x, xp, fp)
  if shape(xp) != shape(fp) or ndim(xp) != 1:
    raise ValueError("xp and fp must be one-dimensional arrays of equal size")
  x_arr, xp_arr = util._promote_dtypes_inexact(x, xp)
  fp_arr, = util._promote_dtypes_inexact(fp)
  del x, xp, fp

  if dtypes.issubdtype(x_arr.dtype, np.complexfloating):
    raise ValueError("jnp.interp: complex x values not supported.")

  if period is not None:
    if ndim(period) != 0:
      raise ValueError(f"period must be a scalar; got {period}")
    period = ufuncs.abs(period)
    x_arr = x_arr % period
    xp_arr = xp_arr % period
    xp_arr, fp_arr = lax.sort_key_val(xp_arr, fp_arr)
    xp_arr = concatenate([xp_arr[-1:] - period, xp_arr, xp_arr[:1] + period])
    fp_arr = concatenate([fp_arr[-1:], fp_arr, fp_arr[:1]])

  i = clip(searchsorted(xp_arr, x_arr, side='right'), 1, len(xp_arr) - 1)
  df = fp_arr[i] - fp_arr[i - 1]
  dx = xp_arr[i] - xp_arr[i - 1]
  delta = x_arr - xp_arr[i - 1]

  epsilon = np.spacing(np.finfo(xp_arr.dtype).eps)
  dx0 = lax.abs(dx) <= epsilon  # Prevent NaN gradients when `dx` is small.
  f = where(dx0, fp_arr[i - 1], fp_arr[i - 1] + (delta / where(dx0, 1, dx)) * df)

  left_arr: ArrayLike = fp_arr[0] if left is None else left
  right_arr: ArrayLike = fp_arr[-1] if right is None else right

  if period is None:
    f = where(x_arr < xp_arr[0], left_arr, f)
    f = where(x_arr > xp_arr[-1], right_arr, f)
  return f
