def _update_disable_jit_thread_local(val):
  lib.jax_jit.thread_local_state().disable_jit = val
