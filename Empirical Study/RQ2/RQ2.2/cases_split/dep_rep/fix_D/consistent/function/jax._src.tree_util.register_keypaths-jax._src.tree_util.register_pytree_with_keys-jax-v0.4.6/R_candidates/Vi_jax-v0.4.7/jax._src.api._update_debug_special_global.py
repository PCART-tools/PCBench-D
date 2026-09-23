def _update_debug_special_global(_):
  if config._read("jax_debug_nans") or config._read("jax_debug_infs"):
    jax_jit.global_state().post_hook = _nan_check_posthook
  else:
    jax_jit.global_state().post_hook = None
