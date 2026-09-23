@partial(jit, static_argnames=('invert',))
def _in1d(ar1: ArrayLike, ar2: ArrayLike, invert: bool) -> Array:
  _check_arraylike("in1d", ar1, ar2)
  ar1_flat = ravel(ar1)
  ar2_flat = ravel(ar2)
  # Note: an algorithm based on searchsorted has better scaling, but in practice
  # is very slow on accelerators because it relies on lax control flow. If XLA
  # ever supports binary search natively, we should switch to this:
  #   ar2_flat = jnp.sort(ar2_flat)
  #   ind = jnp.searchsorted(ar2_flat, ar1_flat)
  #   if invert:
  #     return ar1_flat != ar2_flat[ind]
  #   else:
  #     return ar1_flat == ar2_flat[ind]
  if invert:
    return (ar1_flat[:, None] != ar2_flat[None, :]).all(-1)
  else:
    return (ar1_flat[:, None] == ar2_flat[None, :]).any(-1)
