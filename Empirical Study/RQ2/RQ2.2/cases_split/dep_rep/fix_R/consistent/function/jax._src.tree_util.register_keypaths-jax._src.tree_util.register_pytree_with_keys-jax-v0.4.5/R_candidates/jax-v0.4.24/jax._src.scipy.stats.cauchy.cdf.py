@implements(osp_stats.cauchy.cdf, update_doc=False)
def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = promote_args_inexact("cauchy.cdf", x, loc, scale)
  pi = _lax_const(x, np.pi)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  return lax.add(_lax_const(x, 0.5), lax.mul(lax.div(_lax_const(x, 1.), pi), arctan(scaled_x)))
