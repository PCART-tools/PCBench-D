def _update_debug_special_thread_local(_):
  if (getattr(config_thread_local_state, "jax_debug_nans", False) or
      getattr(config_thread_local_state, "jax_debug_infs", False)):
    jax_jit.thread_local_state().post_hook = _nan_check_posthook
  else:
    jax_jit.thread_local_state().post_hook = None
