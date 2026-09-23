@_wraps(np.vstack)
def vstack(tup):
  if isinstance(tup, (np.ndarray, ndarray)):
    arrs = jax.vmap(atleast_2d)(tup)
  else:
    arrs = [atleast_2d(m) for m in tup]
  return concatenate(arrs, axis=0)
