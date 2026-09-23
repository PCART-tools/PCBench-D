@partial(jit, static_argnums=(2,))
def _bernoulli(key, p, shape) -> Array:
  if shape is None:
    # TODO: Use the named part of `p` as well
    shape = np.shape(p)
  else:
    _check_shape("bernoulli", shape, np.shape(p))

  return uniform(key, shape, lax.dtype(p)) < p
