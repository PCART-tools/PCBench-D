def _maybe_put(x):
  if isinstance(x, np.ndarray):
    return jax.device_put(x, jax.devices('cpu')[0])
  else:
    return x
