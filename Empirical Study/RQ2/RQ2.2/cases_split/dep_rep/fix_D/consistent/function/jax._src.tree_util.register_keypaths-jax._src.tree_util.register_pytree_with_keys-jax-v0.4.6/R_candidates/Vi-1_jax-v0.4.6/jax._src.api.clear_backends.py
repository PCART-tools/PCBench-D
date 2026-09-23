def clear_backends():
  """
  Clear all backend clients so that new backend clients can be created later.
  """
  xb._clear_backends()
  jax.lib.xla_bridge._backends = {}
  dispatch.xla_callable.cache_clear()  # type: ignore
  dispatch.xla_primitive_callable.cache_clear()
  _cpp_jit_cache.clear()
  jax_jit.CompiledFunctionCache.clear_all()
  pjit._pjit_lower_cached.cache_clear()
  pjit._create_pjit_jaxpr.cache_clear()
  pjit._cpp_pjit_cache.clear()
  xc._xla.PjitFunctionCache.clear_all()
