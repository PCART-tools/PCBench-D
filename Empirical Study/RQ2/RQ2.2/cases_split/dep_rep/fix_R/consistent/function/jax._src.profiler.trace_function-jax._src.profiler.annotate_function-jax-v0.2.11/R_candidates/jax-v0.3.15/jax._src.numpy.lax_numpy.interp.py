@_wraps(np.interp)
@jit
def interp(x, xp, fp, left=None, right=None, period=None):
  _check_arraylike("interp", x, xp, fp)
  if shape(xp) != shape(fp) or ndim(xp) != 1:
    raise ValueError("xp and fp must be one-dimensional arrays of equal size")
  x, xp = _promote_dtypes_inexact(x, xp)
  fp, = _promote_dtypes_inexact(fp)

  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise ValueError("jnp.interp: complex x values not supported.")

  if period is not None:
    if ndim(period) != 0:
      raise ValueError(f"period must be a scalar; got {period}")
    period = abs(period)
    x = x % period
    xp = xp % period
    xp, fp = lax.sort_key_val(xp, fp)
    xp = concatenate([xp[-1:] - period, xp, xp[:1] + period])
    fp = concatenate([fp[-1:], fp, fp[:1]])

  i = clip(searchsorted(xp, x, side='right'), 1, len(xp) - 1)
  df = fp[i] - fp[i - 1]
  dx = xp[i] - xp[i - 1]
  delta = x - xp[i - 1]
  f = where((dx == 0), fp[i], fp[i - 1] + (delta / dx) * df)

  if period is None:
    f = where(x < xp[0], fp[0] if left is None else left, f)
    f = where(x > xp[-1], fp[-1] if right is None else right, f)
  return f
