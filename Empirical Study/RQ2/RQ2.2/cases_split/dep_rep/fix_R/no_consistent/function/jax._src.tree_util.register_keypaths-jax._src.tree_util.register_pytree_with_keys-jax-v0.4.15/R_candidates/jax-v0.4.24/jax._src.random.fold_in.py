def fold_in(key: KeyArrayLike, data: IntegerArray) -> KeyArray:
  """Folds in data to a PRNG key to form a new PRNG key.

  Args:
    key: a PRNG key (from ``PRNGKey``, ``split``, ``fold_in``).
    data: a 32bit integer representing data to be folded in to the key.

  Returns:
    A new PRNG key that is a deterministic function of the inputs and is
    statistically safe for producing a stream of new pseudo-random values.
  """
  key, wrapped = _check_prng_key("fold_in", key, error_on_batched=True)
  if np.ndim(data):
    raise TypeError("fold_in accepts a scalar, but was given an array of"
                    f"shape {np.shape(data)} != (). Use jax.vmap for batching.")
  key_out = prng.random_fold_in(key, jnp.uint32(data))
  return _return_prng_keys(wrapped, key_out)
