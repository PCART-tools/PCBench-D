def _update_disable_jit_global(val):
  lib.jax_jit.global_state().disable_jit = val
