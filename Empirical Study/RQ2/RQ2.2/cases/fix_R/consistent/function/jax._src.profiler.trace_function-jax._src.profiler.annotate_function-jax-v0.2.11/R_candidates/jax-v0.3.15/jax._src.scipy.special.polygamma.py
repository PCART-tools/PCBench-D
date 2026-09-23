@_wraps(osp_special.polygamma, module='scipy.special', update_doc=False)
def polygamma(n, x):
  assert jnp.issubdtype(lax.dtype(n), jnp.integer)
  n, x = _promote_args_inexact("polygamma", n, x)
  shape = lax.broadcast_shapes(n.shape, x.shape)
  return _polygamma(jnp.broadcast_to(n, shape), jnp.broadcast_to(x, shape))
