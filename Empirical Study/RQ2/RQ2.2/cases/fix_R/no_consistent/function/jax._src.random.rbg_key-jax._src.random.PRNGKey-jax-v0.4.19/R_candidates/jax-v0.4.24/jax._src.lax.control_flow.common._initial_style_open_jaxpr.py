@weakref_lru_cache
def _initial_style_open_jaxpr(fun: Callable, in_tree, in_avals,
                              primitive_name: str | None = None):
  wrapped_fun, out_tree = flatten_fun_nokwargs(lu.wrap_init(fun), in_tree)
  debug = pe.debug_info(fun, in_tree, out_tree, False,
                        primitive_name or "<unknown>")
  jaxpr, _, consts, attrs_tracked = pe.trace_to_jaxpr_dynamic(
      wrapped_fun, in_avals, debug)
  return jaxpr, consts, out_tree(), attrs_tracked
