def clear_backends():
  """
  Clear all backend clients so that new backend clients can be created later.
  """

  if xc._version < 79:
    raise RuntimeError("clear_backends is not supported in the jaxlib used."
                       "Please update your jaxlib package.")

  xb._clear_backends()
  jax.lib.xla_bridge._backends = {}
  dispatch.xla_callable.cache_clear()  # type: ignore
  dispatch.xla_primitive_callable.cache_clear()
  _cpp_jit_cache.clear()
  jax_jit.CompiledFunctionCache.clear_all()
