def _key(ctor_name: str, seed: Union[int, Array], impl_spec: Optional[str]
         ) -> PRNGKeyArray:
  impl = resolve_prng_impl(impl_spec)
  if hasattr(seed, 'dtype') and jnp.issubdtype(seed.dtype, dtypes.prng_key):
    raise TypeError(
        f"{ctor_name} accepts a scalar seed, but was given a PRNGKeyArray.")
  if np.ndim(seed):
    raise TypeError(
        f"{ctor_name} accepts a scalar seed, but was given an array of "
        f"shape {np.shape(seed)} != (). Use jax.vmap for batching")
  return prng.seed_with_impl(impl, seed)
