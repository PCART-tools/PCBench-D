def _update_jax_memories_global(val):
  lib.jax_jit.global_state().enable_memories = val
