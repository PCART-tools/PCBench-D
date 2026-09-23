def _cpp_jit_clear_cache(self):
  self._clear_cache()
  dispatch.xla_callable.evict_function(self._fun)
