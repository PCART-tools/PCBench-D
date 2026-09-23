@debug_callback_p.def_impl
def debug_callback_impl(*flat_args, callback: Callable[..., Any],
    effect: DebugEffect, in_tree: tree_util.PyTreeDef):
  del effect
  args, kwargs = tree_util.tree_unflatten(in_tree, flat_args)
  out = callback(*args, **kwargs)
  return tree_util.tree_leaves(out)
