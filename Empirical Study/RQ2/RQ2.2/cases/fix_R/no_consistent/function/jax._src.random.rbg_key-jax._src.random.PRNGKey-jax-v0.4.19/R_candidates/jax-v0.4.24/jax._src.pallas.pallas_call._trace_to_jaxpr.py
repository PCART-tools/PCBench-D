@weakref_lru_cache
def _trace_to_jaxpr(fun: Callable, grid_spec: GridSpec, flat_in_avals,
                    flat_out_avals, in_tree, out_tree):
  avals, grid_mapping = grid_spec.get_grid_mapping(flat_in_avals, in_tree,
                                                   flat_out_avals, out_tree)
  jaxpr_flat_avals, jaxpr_in_tree = tree_util.tree_flatten(avals)
  wrapped_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
      lu.wrap_init(fun), jaxpr_in_tree)
  debug = pe.debug_info(fun, jaxpr_in_tree, out_tree_thunk, False, "pallas_call")
  jaxpr, _, consts, () = pe.trace_to_jaxpr_dynamic(wrapped_fun, jaxpr_flat_avals, debug)
  jaxpr = _hoist_consts_to_refs(jaxpr)
  return grid_mapping, jaxpr, consts, out_tree_thunk()
