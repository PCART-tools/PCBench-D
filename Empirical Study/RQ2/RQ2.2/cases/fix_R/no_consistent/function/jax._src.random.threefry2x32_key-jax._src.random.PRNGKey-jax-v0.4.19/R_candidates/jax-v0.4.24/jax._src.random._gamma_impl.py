def _gamma_impl(key, a, *, log_space, use_vmap=False):
  # split key to match the shape of a
  a_shape = jnp.shape(a)
  split_count = math.prod(a_shape[key.ndim:])
  keys = key.flatten()
  keys = vmap(_split, in_axes=(0, None))(keys, split_count)
  keys = keys.flatten()
  alphas = a.flatten()

  if use_vmap:
    samples = vmap(partial(_gamma_one, log_space=log_space))(keys, alphas)
  else:
    samples = lax.map(
        lambda args: _gamma_one(*args, log_space=log_space), (keys, alphas))

  return jnp.reshape(samples, a_shape)
