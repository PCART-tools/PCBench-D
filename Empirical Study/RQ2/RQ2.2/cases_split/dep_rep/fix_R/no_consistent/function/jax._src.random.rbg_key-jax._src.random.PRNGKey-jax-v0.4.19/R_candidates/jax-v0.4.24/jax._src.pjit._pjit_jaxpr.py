def _pjit_jaxpr(fun, out_shardings_thunk, out_layouts_thunk, in_type, debug_info,
                device_or_backend_set, out_tree, result_paths, inline):
  jaxpr, final_consts, out_type, attrs_tracked = _create_pjit_jaxpr(
      fun, in_type, debug_info, result_paths, IgnoreKey(inline))
  canonicalized_out_shardings_flat, out_layouts_flat = _check_and_canonicalize_out_shardings(
      out_shardings_thunk, out_layouts_thunk, out_tree, tuple(out_type),
      jaxpr.jaxpr.debug_info, device_or_backend_set)
  return jaxpr, final_consts, canonicalized_out_shardings_flat, out_layouts_flat, attrs_tracked
