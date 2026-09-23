def _get_cpp_global_cache(pjit_has_explicit_sharding):
  if pjit_has_explicit_sharding:
    return xc._xla.PjitFunctionCache()
  else:
    return _cpp_pjit_cache
