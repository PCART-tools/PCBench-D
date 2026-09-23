@custom_derivatives.custom_jvp
@_wraps(osp_special.zeta, module='scipy.special')
def zeta(x: ArrayLike, q: Optional[ArrayLike] = None) -> Array:
  if q is None:
    raise NotImplementedError(
      "Riemann zeta function not implemented; pass q != None to compute the Hurwitz Zeta function.")
  x, q = promote_args_inexact("zeta", x, q)
  return lax.zeta(x, q)
