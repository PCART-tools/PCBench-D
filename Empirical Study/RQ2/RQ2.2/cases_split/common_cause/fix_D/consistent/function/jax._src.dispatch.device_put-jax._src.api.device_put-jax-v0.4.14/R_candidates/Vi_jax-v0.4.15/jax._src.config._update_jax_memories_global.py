def _update_jax_memories_global(val):
  if xla_extension_version >= 190:
    lib.jax_jit.global_state().enable_memories = val
