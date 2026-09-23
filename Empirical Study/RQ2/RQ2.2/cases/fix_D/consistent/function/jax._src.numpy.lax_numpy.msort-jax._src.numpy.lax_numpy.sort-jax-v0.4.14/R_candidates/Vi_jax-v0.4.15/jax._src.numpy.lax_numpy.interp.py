@util._wraps(np.interp,
  lax_description=_dedent("""
    In addition to constant interpolation supported by NumPy, jnp.interp also
    supports left='extrapolate' and right='extrapolate' to indicate linear
    extrapolation instead."""))
def interp(x: ArrayLike, xp: ArrayLike, fp: ArrayLike,
           left: ArrayLike | str | None = None,
           right: ArrayLike | str | None = None,
           period: ArrayLike | None = None) -> Array:
  static_argnames = []
  if isinstance(left, str) or left is None:
    static_argnames.append('left')
  if isinstance(right, str) or right is None:
    static_argnames.append('right')
  if period is None:
    static_argnames.append('period')
  jitted_interp = jit(_interp, static_argnames=static_argnames)
  return jitted_interp(x, xp, fp, left, right, period)
