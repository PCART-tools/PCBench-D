@implements(osp_stats.cauchy.ppf, update_doc=False)
def ppf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  q, loc, scale = promote_args_inexact("cauchy.ppf", q, loc, scale)
  pi = _lax_const(q, np.pi)
  half_pi = _lax_const(q, np.pi / 2)
  unscaled = lax.tan(lax.sub(lax.mul(pi, q), half_pi))
  return lax.add(lax.mul(unscaled, scale), loc)
