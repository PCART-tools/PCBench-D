def PRNGKey(seed: Union[int, Array], *,
            impl: Optional[str] = None) -> KeyArray:
  """Create a pseudo-random number generator (PRNG) key given an integer seed.

  The resulting key carries the default PRNG implementation, as
  determined by the optional ``impl`` argument or, otherwise, by the
  ``jax_default_prng_impl`` config flag.

  Args:
    seed: a 64- or 32-bit integer used as the value of the key.
    impl: optional string specifying the PRNG implementation (e.g.
      ``'threefry2x32'``)

  Returns:
    A PRNG key, consumable by random functions as well as ``split``
    and ``fold_in``.
  """
  return _return_prng_keys(True, _key('PRNGKey', seed, impl))
