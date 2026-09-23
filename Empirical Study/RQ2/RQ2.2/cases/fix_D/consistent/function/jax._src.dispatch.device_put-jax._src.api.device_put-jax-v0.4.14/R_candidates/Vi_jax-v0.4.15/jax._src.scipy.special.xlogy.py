@custom_derivatives.custom_jvp
@_wraps(osp_special.xlogy, module='scipy.special')
def xlogy(x: ArrayLike, y: ArrayLike) -> Array:
  # Note: xlogy(0, 0) should return 0 according to the function documentation.
  x, y = promote_args_inexact("xlogy", x, y)
  x_ok = x != 0.
  return jnp.where(x_ok, lax.mul(x, lax.log(y)), jnp.zeros_like(x))
