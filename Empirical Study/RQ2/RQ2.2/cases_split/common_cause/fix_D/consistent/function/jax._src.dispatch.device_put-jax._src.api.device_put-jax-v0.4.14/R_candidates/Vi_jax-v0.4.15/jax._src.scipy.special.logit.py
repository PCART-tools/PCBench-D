@custom_derivatives.custom_jvp
@_wraps(osp_special.logit, module='scipy.special', update_doc=False)
def logit(x: ArrayLike) -> Array:
  x, = promote_args_inexact("logit", x)
  return lax.log(lax.div(x, lax.sub(_lax_const(x, 1), x)))
