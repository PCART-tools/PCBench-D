def _update_jax_array_thread_local(val):
  if val is not None and not val:
    warnings.warn(
        'DeviceArray, ShardedDeviceArray, and GlobalDeviceArray have been '
        'deprecated. Please use `jax.Array`. See '
        'https://jax.readthedocs.io/en/latest/jax_array_migration.html on how '
        'to migrate to `jax.Array`.', DeprecationWarning)
  lib.jax_jit.thread_local_state().jax_array = val
