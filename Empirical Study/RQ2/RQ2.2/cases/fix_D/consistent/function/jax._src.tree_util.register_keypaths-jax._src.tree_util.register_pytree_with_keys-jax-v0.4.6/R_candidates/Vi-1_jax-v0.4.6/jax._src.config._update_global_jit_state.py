def _update_global_jit_state(**kw):
  gs = jax_jit.global_state()
  context = gs.extra_jit_context or _GlobalExtraJitContext()
  gs.extra_jit_context = context._replace(**kw)
