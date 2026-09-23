def debug_callback_jvp_rule(*flat_args, callback: Callable[..., Any],
    effect: DebugEffect, in_tree: tree_util.PyTreeDef):
  del flat_args, callback, effect, in_tree
  # TODO(sharadmv): link to relevant documentation when it exists
  raise ValueError(
      "JVP doesn't support debugging callbacks. "
      "Instead, you can use them with `jax.custom_jvp` or `jax.custom_vjp`.")
