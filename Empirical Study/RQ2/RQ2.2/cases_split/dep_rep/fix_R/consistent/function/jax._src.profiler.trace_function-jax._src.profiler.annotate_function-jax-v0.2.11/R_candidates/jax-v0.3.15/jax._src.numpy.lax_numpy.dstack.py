@_wraps(np.dstack)
def dstack(tup):
  if isinstance(tup, (np.ndarray, ndarray)):
    arrs = jax.vmap(atleast_3d)(tup)
  else:
    arrs = [atleast_3d(m) for m in tup]
  return concatenate(arrs, axis=2)
