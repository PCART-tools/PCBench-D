@_wraps(np.in1d, lax_description="""
In the JAX version, the `assume_unique` argument is not referenced.
""")
@partial(jit, static_argnames=('assume_unique', 'invert',))
def in1d(ar1, ar2, assume_unique=False, invert=False):  # noqa: F811
  del assume_unique  # unused
  _check_arraylike("in1d", ar1, ar2)
  ar1 = ravel(ar1)
  ar2 = ravel(ar2)
  # Note: an algorithm based on searchsorted has better scaling, but in practice
  # is very slow on accelerators because it relies on lax control flow. If XLA
  # ever supports binary search natively, we should switch to this:
  #   ar2 = jnp.sort(ar2)
  #   ind = jnp.searchsorted(ar2, ar1)
  #   if invert:
  #     return ar1 != ar2[ind]
  #   else:
  #     return ar1 == ar2[ind]
  if invert:
    return (ar1[:, None] != ar2[None, :]).all(-1)
  else:
    return (ar1[:, None] == ar2[None, :]).any(-1)
