def debug_callback_transpose_rule(*flat_args, callback: Callable[..., Any],
    effect: DebugEffect, in_tree: tree_util.PyTreeDef):
  del flat_args, callback, effect, in_tree
  raise ValueError("Transpose doesn't support debugging callbacks.")
