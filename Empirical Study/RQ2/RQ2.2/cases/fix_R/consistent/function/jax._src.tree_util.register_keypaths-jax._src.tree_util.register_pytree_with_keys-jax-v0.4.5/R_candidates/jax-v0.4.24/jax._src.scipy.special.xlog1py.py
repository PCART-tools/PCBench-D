@custom_derivatives.custom_jvp
@implements(osp_special.xlog1py, module='scipy.special', update_doc=False)
def xlog1py(x: ArrayLike, y: ArrayLike) -> Array:
  # Note: xlog1py(0, -1) should return 0 according to the function documentation.
  x, y = promote_args_inexact("xlog1py", x, y)
  x_ok = x != 0.
  return jnp.where(x_ok, lax.mul(x, lax.log1p(y)), jnp.zeros_like(x))
