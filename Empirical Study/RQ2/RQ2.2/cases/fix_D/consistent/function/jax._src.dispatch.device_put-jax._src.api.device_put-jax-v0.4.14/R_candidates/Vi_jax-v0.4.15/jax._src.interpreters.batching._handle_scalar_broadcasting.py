def _handle_scalar_broadcasting(nd, x, d):
  if d is not_mapped or nd == np.ndim(x):
    return x
  else:
    return jax.lax.expand_dims(x, tuple(range(np.ndim(x), nd)))
