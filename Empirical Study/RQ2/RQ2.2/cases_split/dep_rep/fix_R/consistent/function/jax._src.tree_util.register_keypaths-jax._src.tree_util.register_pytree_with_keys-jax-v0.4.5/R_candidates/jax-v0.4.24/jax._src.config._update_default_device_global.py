def _update_default_device_global(val):
  lib.jax_jit.global_state().default_device = val
