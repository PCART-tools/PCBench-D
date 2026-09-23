def default_prng_impl():
  """Get the default PRNG implementation.

  The default implementation is determined by ``config.jax_default_prng_impl``,
  which specifies it by name. This function returns the corresponding
  ``jax.prng.PRNGImpl`` instance.
  """
  impl_name = config.jax_default_prng_impl
  assert impl_name in PRNG_IMPLS, impl_name
  return PRNG_IMPLS[impl_name]
