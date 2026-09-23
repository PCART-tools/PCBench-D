@_wraps(osp_special.xlog1py, module='scipy.special', update_doc=False)
def xlog1py(x, y):
  x, y = _promote_args_inexact("xlog1py", x, y)
  x_ok = x != 0.
  safe_x = jnp.where(x_ok, x, 1.)
  safe_y = jnp.where(x_ok, y, 1.)
  return jnp.where(x_ok, lax.mul(safe_x, lax.log1p(safe_y)), jnp.zeros_like(x))
