def shuffle(key: KeyArray, x: Array, axis: int = 0) -> jnp.ndarray:
  """Shuffle the elements of an array uniformly at random along an axis.

  Args:
    key: a PRNG key used as the random key.
    x: the array to be shuffled.
    axis: optional, an int axis along which to shuffle (default 0).

  Returns:
    A shuffled version of x.
  """
  msg = ("jax.random.shuffle is deprecated and will be removed in a future release. "
         "Use jax.random.permutation with independent=True.")
  warnings.warn(msg, FutureWarning)
  key, _ = _check_prng_key(key)
  return _shuffle(key, x, axis)  # type: ignore
