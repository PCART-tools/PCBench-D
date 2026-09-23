@debug_callback_p.def_effectful_abstract_eval
def debug_callback_abstract_eval(*flat_avals, callback: Callable[..., Any],
    effect: DebugEffect, in_tree: tree_util.PyTreeDef):
  del flat_avals, callback, in_tree
  return [], {effect}
