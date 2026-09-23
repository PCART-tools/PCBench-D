@implements(np.polyfit, lax_description=_POLYFIT_DOC)
@partial(jit, static_argnames=('deg', 'rcond', 'full', 'cov'))
def polyfit(x: Array, y: Array, deg: int, rcond: float | None = None,
            full: bool = False, w: Array | None = None, cov: bool = False
            ) -> Array | tuple[Array, ...]:
  check_arraylike("polyfit", x, y)
  deg = core.concrete_or_error(int, deg, "deg must be int")
  order = deg + 1
  # check arguments
  if deg < 0:
    raise ValueError("expected deg >= 0")
  if x.ndim != 1:
    raise TypeError("expected 1D vector for x")
  if x.size == 0:
    raise TypeError("expected non-empty vector for x")
  if y.ndim < 1 or y.ndim > 2:
    raise TypeError("expected 1D or 2D array for y")
  if x.shape[0] != y.shape[0]:
    raise TypeError("expected x and y to have same length")

  # set rcond
  if rcond is None:
    rcond = len(x) * finfo(x.dtype).eps
  rcond = core.concrete_or_error(float, rcond, "rcond must be float")
  # set up least squares equation for powers of x
  lhs = vander(x, order)
  rhs = y

  # apply weighting
  if w is not None:
    check_arraylike("polyfit", w)
    w, = promote_dtypes_inexact(w)
    if w.ndim != 1:
      raise TypeError("expected a 1-d array for weights")
    if w.shape[0] != y.shape[0]:
      raise TypeError("expected w and y to have the same length")
    lhs *= w[:, np.newaxis]
    if rhs.ndim == 2:
      rhs *= w[:, np.newaxis]
    else:
      rhs *= w

  # scale lhs to improve condition number and solve
  scale = sqrt((lhs*lhs).sum(axis=0))
  lhs /= scale[np.newaxis,:]
  c, resids, rank, s = linalg.lstsq(lhs, rhs, rcond)
  c = (c.T/scale).T  # broadcast scale coefficients

  if full:
    return c, resids, rank, s, asarray(rcond)
  elif cov:
    Vbase = linalg.inv(dot(lhs.T, lhs))
    Vbase /= outer(scale, scale)
    if cov == "unscaled":
      fac = 1
    else:
      if len(x) <= order:
        raise ValueError("the number of data points must exceed order "
                            "to scale the covariance matrix")
      fac = resids / (len(x) - order)
      fac = fac[0] #making np.array() of shape (1,) to int
    if y.ndim == 1:
      return c, Vbase * fac
    else:
      return c, Vbase[:, :, np.newaxis] * fac
  else:
    return c
