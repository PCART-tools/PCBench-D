@implements(osp_special.beta, module='scipy.special')
def beta(x: ArrayLike, y: ArrayLike) -> Array:
  x, y = promote_args_inexact("beta", x, y)
  return lax.exp(betaln(x, y))
