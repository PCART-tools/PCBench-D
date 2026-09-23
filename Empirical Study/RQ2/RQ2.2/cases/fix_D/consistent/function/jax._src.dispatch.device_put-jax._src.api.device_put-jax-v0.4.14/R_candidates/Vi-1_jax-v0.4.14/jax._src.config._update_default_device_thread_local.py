def _update_default_device_thread_local(val):
  lib.jax_jit.thread_local_state().default_device = val
