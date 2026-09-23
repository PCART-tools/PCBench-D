@implements(osp_special.polygamma, module='scipy.special', update_doc=False)
def polygamma(n: ArrayLike, x: ArrayLike) -> Array:
  assert jnp.issubdtype(lax.dtype(n), jnp.integer)
  n_arr, x_arr = promote_args_inexact("polygamma", n, x)
  return lax.polygamma(n_arr, x_arr)
