def PRNGKey(seed: int) -> KeyArray:
  """Create a pseudo-random number generator (PRNG) key given an integer seed.

  The resulting key carries the default PRNG implementation, as
  determined by the ``jax_default_prng_impl`` config flag.

  Args:
    seed: a 64- or 32-bit integer used as the value of the key.

  Returns:
    A PRNG key, consumable by random functions as well as ``split``
    and ``fold_in``.

  """
  impl = default_prng_impl()
  key = prng.seed_with_impl(impl, seed)
  return _return_prng_keys(True, key)
