@_wraps(osp_special.xlogy, module='scipy.special')
def xlogy(x: ArrayLike, y: ArrayLike) -> Array:
  x, y = _promote_args_inexact("xlogy", x, y)
  x_ok = x != 0.
  safe_x = jnp.where(x_ok, x, 1.)
  safe_y = jnp.where(x_ok, y, 1.)
  return jnp.where(x_ok, lax.mul(safe_x, lax.log(safe_y)), jnp.zeros_like(x))
