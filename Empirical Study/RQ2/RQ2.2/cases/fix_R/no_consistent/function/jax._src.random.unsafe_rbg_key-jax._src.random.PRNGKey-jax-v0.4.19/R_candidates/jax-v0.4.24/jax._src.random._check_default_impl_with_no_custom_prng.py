def _check_default_impl_with_no_custom_prng(impl, name):
  default_impl = default_prng_impl()
  default_name = config.default_prng_impl.value
  if not config.enable_custom_prng.value and default_impl is not impl:
    raise RuntimeError('jax_enable_custom_prng must be enabled in order '
                       f'to seed an RNG with an implementation "{name}" '
                       f'differing from the default "{default_name}".')
