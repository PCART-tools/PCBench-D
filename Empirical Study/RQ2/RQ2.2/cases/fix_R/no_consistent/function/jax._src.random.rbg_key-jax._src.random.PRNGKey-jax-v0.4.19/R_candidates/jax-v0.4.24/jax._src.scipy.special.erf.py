@implements(osp_special.erf, module='scipy.special', skip_params=["out"],
        lax_description="Note that the JAX version does not support complex inputs.")
def erf(x: ArrayLike) -> Array:
  x, = promote_args_inexact("erf", x)
  return lax.erf(x)
