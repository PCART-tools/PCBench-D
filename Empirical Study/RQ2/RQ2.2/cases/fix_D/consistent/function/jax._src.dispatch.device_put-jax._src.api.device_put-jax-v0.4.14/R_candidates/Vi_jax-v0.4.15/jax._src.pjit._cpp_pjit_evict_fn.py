def _cpp_pjit_evict_fn(self):
  self._clear_cache()
  _create_pjit_jaxpr.evict_function(self._fun)  # type: ignore
