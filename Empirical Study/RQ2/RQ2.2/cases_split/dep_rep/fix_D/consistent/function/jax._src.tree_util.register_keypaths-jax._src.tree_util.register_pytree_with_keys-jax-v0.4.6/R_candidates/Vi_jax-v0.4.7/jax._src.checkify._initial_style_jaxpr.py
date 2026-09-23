@weakref_lru_cache
def _initial_style_jaxpr(fun, in_tree, in_avals):
  # like control_flow._initial_style_jaxpr, but use flatten_fun not _nokwargs
  fun_, out_tree = flatten_fun(lu.wrap_init(fun), in_tree)
  debug = pe.debug_info(fun, in_tree, out_tree, False, 'checkify')
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(fun_, in_avals, debug)
  return jaxpr, consts, out_tree()
