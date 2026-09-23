@weakref_lru_cache
def _initial_style_jaxpr(fun, in_tree, in_avals):
  fun_, out_tree_thunk = api_util.flatten_fun_nokwargs(lu.wrap_init(fun),
      tree_util.treedef_tuple((in_tree,)))
  debug = pe.debug_info(fun_, in_tree, out_tree_thunk, False, 'run_state')
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(fun_, in_avals, debug)
  return jaxpr, consts, out_tree_thunk()
