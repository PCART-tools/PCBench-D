@_wraps(osp_special.polygamma, module='scipy.special', update_doc=False)
def polygamma(n: ArrayLike, x: ArrayLike) -> Array:
  assert jnp.issubdtype(lax.dtype(n), jnp.integer)
  n_arr, x_arr = promote_args_inexact("polygamma", n, x)
  shape = lax.broadcast_shapes(n_arr.shape, x_arr.shape)
  return _polygamma(jnp.broadcast_to(n_arr, shape), jnp.broadcast_to(x_arr, shape))
