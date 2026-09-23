def _fold_in(key: KeyArray, data: IntegerArray) -> KeyArray:
  # Alternative to fold_in() to use within random samplers.
  # TODO(frostig): remove and use fold_in() once we always enable_custom_prng
  assert jnp.issubdtype(key.dtype, dtypes.prng_key)
  if key.ndim:
    raise TypeError("fold_in accepts a single key, but was given a key array of"
                    f"shape {key.shape} != (). Use jax.vmap for batching.")
  if np.ndim(data):
    raise TypeError("fold_in accepts a scalar, but was given an array of"
                    f"shape {np.shape(data)} != (). Use jax.vmap for batching.")
  return prng.random_fold_in(key, jnp.uint32(data))
