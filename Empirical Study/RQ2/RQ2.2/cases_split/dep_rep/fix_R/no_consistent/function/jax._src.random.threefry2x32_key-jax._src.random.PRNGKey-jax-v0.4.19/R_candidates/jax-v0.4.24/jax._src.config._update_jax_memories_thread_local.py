def _update_jax_memories_thread_local(val):
  lib.jax_jit.thread_local_state().enable_memories = val
