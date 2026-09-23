def _update_jax_array_global(val):
  if val is not None and not val:
    raise ValueError(
        'jax.config.jax_array cannot be disabled after jax 0.4.7 release.'
        ' Please downgrade to jax and jaxlib 0.4.6 if you want to disable'
        ' jax.config.jax_array.')
  if xla_extension_version < 141:
    lib.jax_jit.global_state().jax_array = val
