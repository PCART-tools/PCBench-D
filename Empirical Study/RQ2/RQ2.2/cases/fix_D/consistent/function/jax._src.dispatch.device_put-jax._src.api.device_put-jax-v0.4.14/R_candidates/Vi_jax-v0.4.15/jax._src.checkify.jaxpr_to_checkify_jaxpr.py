@weakref_lru_cache
def jaxpr_to_checkify_jaxpr(
    jaxpr: core.ClosedJaxpr, enabled_errors, err_tree: PyTreeDef,
    *flat_err_and_in_vals) -> tuple[core.ClosedJaxpr, PyTreeDef, set[ErrorEffect]]:
  checkify_jaxpr_partial = functools.partial(checkify_jaxpr_flat, jaxpr.jaxpr,
                                             jaxpr.consts, enabled_errors,
                                             err_tree)
  fun = lu.wrap_init(checkify_jaxpr_partial)
  fun, metadata = _flatten_and_get_error_metadata_thunk(fun)

  new_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(fun, flat_err_and_in_vals)
  checked_jaxpr = core.ClosedJaxpr(new_jaxpr, consts)
  out_tree, error_effects = metadata()
  return checked_jaxpr, out_tree, error_effects
