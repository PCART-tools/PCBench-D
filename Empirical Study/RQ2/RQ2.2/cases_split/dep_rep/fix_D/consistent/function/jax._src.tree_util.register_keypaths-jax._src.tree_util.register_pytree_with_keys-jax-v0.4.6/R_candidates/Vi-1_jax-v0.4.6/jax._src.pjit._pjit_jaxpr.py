def _pjit_jaxpr(fun, out_shardings_thunk, global_in_avals, out_tree, api_name):
  jaxpr, final_consts, global_out_avals = _create_pjit_jaxpr(
      fun, global_in_avals, api_name)
  canonicalized_out_shardings_flat = _check_and_canonicalize_out_shardings(
      out_shardings_thunk, out_tree, tuple(global_out_avals))
  # lu.cache needs to be able to create weakrefs to outputs, so we can't return a plain tuple
  return jaxpr, final_consts, canonicalized_out_shardings_flat
