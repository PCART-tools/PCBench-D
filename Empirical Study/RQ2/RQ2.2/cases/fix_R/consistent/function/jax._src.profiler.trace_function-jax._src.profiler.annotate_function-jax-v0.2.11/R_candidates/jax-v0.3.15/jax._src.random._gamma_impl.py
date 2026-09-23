def _gamma_impl(raw_key, a, *, prng_impl, log_space, use_vmap=False):
  a_shape = jnp.shape(a)
  # split key to match the shape of a
  key_ndim = len(raw_key.shape) - len(prng_impl.key_shape)
  key = raw_key.reshape((-1,) + prng_impl.key_shape)
  key = vmap(prng_impl.split, in_axes=(0, None))(key, prod(a_shape[key_ndim:]))
  keys = key.reshape((-1,) + prng_impl.key_shape)
  keys = prng.PRNGKeyArray(prng_impl, keys)
  alphas = jnp.reshape(a, -1)
  if use_vmap:
    samples = vmap(partial(_gamma_one, log_space=log_space))(keys, alphas)
  else:
    samples = lax.map(lambda args: _gamma_one(*args, log_space=log_space), (keys, alphas))

  return jnp.reshape(samples, a_shape)
