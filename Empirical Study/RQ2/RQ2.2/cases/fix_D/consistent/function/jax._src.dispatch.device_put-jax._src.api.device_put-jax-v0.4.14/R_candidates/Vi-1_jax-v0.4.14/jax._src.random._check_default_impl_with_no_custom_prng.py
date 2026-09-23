def _check_default_impl_with_no_custom_prng(impl, name):
  default_impl = default_prng_impl()
  default_name = config.jax_default_prng_impl
  if not config.jax_enable_custom_prng and default_impl is not impl:
    raise RuntimeError('jax_enable_custom_prng must be enabled in order '
                       f'to seed an RNG with an implementation "f{name}" '
                       f'differing from the default "f{default_name}".')
