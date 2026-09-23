def _update_x64_global(val):
  lib.jax_jit.global_state().enable_x64 = val
