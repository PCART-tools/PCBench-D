  def process_primitive(self, primitive, tracers, params):
    if config.debug_key_reuse.value:
      # Import here to avoid circular imports
      from jax.experimental.key_reuse._core import call_impl_with_key_reuse_checks  # pytype: disable=import-error
      return call_impl_with_key_reuse_checks(primitive, primitive.impl, *tracers, **params)
    else:
      return primitive.impl(*tracers, **params)
