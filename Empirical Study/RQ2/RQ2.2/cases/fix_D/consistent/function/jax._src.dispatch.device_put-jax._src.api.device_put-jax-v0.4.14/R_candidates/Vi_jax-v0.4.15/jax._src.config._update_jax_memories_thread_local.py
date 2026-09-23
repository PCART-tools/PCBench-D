def _update_jax_memories_thread_local(val):
  if xla_extension_version >= 190:
    lib.jax_jit.thread_local_state().enable_memories = val
