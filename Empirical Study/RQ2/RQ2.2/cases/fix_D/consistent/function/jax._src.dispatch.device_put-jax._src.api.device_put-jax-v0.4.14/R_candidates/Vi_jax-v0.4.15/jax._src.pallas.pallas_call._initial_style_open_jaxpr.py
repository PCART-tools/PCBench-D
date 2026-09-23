@weakref_lru_cache
def _initial_style_open_jaxpr(fun: Callable, in_tree, in_avals,
                              primitive_name: str | None = None):
  wrapped_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
      lu.wrap_init(fun), in_tree)
  debug = pe.debug_info(fun, in_tree, out_tree_thunk, False,
                        primitive_name or "<unknown>")
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, in_avals, debug)
  jaxpr = for_loop._hoist_consts_to_refs(jaxpr)
  return jaxpr, consts, out_tree_thunk()
