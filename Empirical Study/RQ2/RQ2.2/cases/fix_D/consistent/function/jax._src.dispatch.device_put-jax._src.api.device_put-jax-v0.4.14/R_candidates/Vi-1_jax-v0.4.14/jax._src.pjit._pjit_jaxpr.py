def _pjit_jaxpr(fun, out_shardings_thunk, in_type, debug_info,
                device_or_backend_set, out_tree, result_paths):
  jaxpr, final_consts, out_type = _create_pjit_jaxpr(
      fun, in_type, debug_info, result_paths)
  canonicalized_out_shardings_flat = _check_and_canonicalize_out_shardings(
      out_shardings_thunk, out_tree, tuple(out_type), jaxpr.jaxpr.debug_info,
      device_or_backend_set)
  # lu.cache needs to be able to create weakrefs to outputs, so we can't return a plain tuple
  return jaxpr, final_consts, canonicalized_out_shardings_flat
