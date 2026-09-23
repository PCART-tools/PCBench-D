@_wraps(osp_special.entr, module='scipy.special')
def entr(x):
  x, = _promote_args_inexact("entr", x)
  return lax.select(lax.lt(x, _lax_const(x, 0)),
                    lax.full_like(x, -np.inf),
                    lax.neg(xlogy(x, x)))
