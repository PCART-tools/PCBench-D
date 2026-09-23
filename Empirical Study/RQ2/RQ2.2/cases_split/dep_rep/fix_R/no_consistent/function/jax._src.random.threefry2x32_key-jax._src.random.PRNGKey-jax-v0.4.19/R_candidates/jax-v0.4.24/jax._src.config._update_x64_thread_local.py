def _update_x64_thread_local(val):
  lib.jax_jit.thread_local_state().enable_x64 = val
