@_wraps(osp_stats.cauchy.isf, update_doc=False)
def isf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  q, loc, scale = promote_args_inexact("cauchy.isf", q, loc, scale)
  pi = _lax_const(q, np.pi)
  half_pi = _lax_const(q, np.pi / 2)
  unscaled = lax.tan(lax.sub(half_pi, lax.mul(pi, q)))
  return lax.add(lax.mul(unscaled, scale), loc)
