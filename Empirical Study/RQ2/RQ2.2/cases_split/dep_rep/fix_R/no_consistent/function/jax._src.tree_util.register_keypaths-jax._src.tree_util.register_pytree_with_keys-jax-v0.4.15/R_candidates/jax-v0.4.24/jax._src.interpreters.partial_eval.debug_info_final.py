def debug_info_final(fn: lu.WrappedFun, traced_for: str) -> DebugInfo:
  "Make a DebugInfo from data available to final-style primitives like pmap."
  in_tree, out_tree, has_kws = flattened_fun_in_tree(fn) or (None, None, False)
  return debug_info(fn.f, in_tree, out_tree, has_kws, traced_for)
