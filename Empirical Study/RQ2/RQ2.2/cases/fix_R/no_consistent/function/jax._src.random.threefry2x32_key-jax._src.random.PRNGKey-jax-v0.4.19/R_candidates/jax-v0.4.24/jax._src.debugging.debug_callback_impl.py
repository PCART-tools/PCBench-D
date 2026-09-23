@debug_callback_p.def_impl
def debug_callback_impl(*args, callback: Callable[..., Any],
                        effect: DebugEffect):
  del effect
  return callback(*args)
