def _split(key: KeyArray, num: int = 2) -> KeyArray:
  # Alternative to split() to use within random samplers.
  # TODO(frostig): remove and use split(); we no longer need to wait
  # to always enable_custom_prng
  assert isinstance(key, prng.PRNGKeyArray)
  if key.ndim:
    raise TypeError("split accepts a single key, but was given a key array of"
                    f"shape {key.shape} != (). Use jax.vmap for batching.")
  return prng.random_split(key, count=num)
