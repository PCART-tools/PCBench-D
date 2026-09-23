def update_thread_local_jit_state(**kw):
  tls = jax_jit.thread_local_state()
  # After xla_client._version >= 70, the thread_local object will necessarily
  # be initialized when accessed. The following line can be removed when the
  # minimum  jaxlib version is past version 70
  context = tls.extra_jit_context or _ThreadLocalExtraJitContext()
  tmp = context._replace(**kw)
  tls.extra_jit_context = _thread_local_state_cache.canonicalize(tmp)
