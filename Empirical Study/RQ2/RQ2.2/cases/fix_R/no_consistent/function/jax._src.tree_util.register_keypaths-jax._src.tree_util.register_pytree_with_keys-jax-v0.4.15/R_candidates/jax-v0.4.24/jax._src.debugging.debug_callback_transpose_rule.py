def debug_callback_transpose_rule(*flat_args, callback: Callable[..., Any],
    effect: DebugEffect):
  del flat_args, callback, effect
  raise ValueError("Transpose doesn't support debugging callbacks.")
