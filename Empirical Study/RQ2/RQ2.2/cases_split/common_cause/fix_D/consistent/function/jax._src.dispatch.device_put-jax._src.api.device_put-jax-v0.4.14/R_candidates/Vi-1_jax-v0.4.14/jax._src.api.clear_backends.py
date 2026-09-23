def clear_backends():
  """
  Clear all backend clients so that new backend clients can be created later.
  """
  xb._clear_backends()
  xb.local_devices.cache_clear()
  xb.process_count.cache_clear()
  dispatch.xla_primitive_callable.cache_clear()
  pjit._pjit_lower_cached.cache_clear()
  pjit._create_pjit_jaxpr.cache_clear()  # pytype: disable=attribute-error
  pjit._cpp_pjit_cache.clear()
  xc._xla.PjitFunctionCache.clear_all()
