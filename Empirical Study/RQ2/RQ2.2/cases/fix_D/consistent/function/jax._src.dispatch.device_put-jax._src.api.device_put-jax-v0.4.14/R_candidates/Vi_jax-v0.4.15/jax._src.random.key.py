def key(seed: Union[int, Array], *,
        impl: Optional[str] = None) -> PRNGKeyArray:
  """Create a pseudo-random number generator (PRNG) key given an integer seed.

  The result is a scalar array with a key that indicates the default PRNG
  implementation, as determined by the optional ``impl`` argument or,
  otherwise, by the ``jax_default_prng_impl`` config flag.

  Args:
    seed: a 64- or 32-bit integer used as the value of the key.
    impl: optional string specifying the PRNG implementation (e.g.
      ``'threefry2x32'``)

  Returns:
    A scalar PRNG key array, consumable by random functions as well as ``split``
    and ``fold_in``.
  """
  return _key('key', seed, impl)
