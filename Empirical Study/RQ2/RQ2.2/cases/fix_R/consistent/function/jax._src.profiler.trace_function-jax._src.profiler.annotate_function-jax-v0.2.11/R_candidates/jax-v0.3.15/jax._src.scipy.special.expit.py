@api.custom_jvp
@_wraps(osp_special.expit, module='scipy.special', update_doc=False)
def expit(x):
  x, = _promote_args_inexact("expit", x)
  one = _lax_const(x, 1)
  return lax.div(one, lax.add(one, lax.exp(lax.neg(x))))
