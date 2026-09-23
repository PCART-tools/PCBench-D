def breakpoint(*, ordered: bool = False, **kwargs):  # pylint: disable=redefined-builtin
  """Enters a breakpoint at a point in a program."""
  frame_infos = inspect.stack()
  # Filter out internal frames
  frame_infos = [
      frame_info for frame_info in frame_infos
      if traceback_util.include_frame(frame_info.frame)
  ]
  frames = [
      DebuggerFrame.from_frameinfo(frame_info) for frame_info in frame_infos
  ]
  # Throw out first frame corresponding to this function
  frames = frames[1:]
  flat_args, frames_tree = tree_util.tree_flatten(frames)

  def _breakpoint_callback(*flat_args):
    frames = tree_util.tree_unflatten(frames_tree, flat_args)
    thread_id = None
    if threading.current_thread() is not threading.main_thread():
      thread_id = threading.get_ident()
    debugger = get_debugger()
    # Lock here because this could be called from multiple threads at the same
    # time.
    with debug_lock:
      debugger(frames, thread_id, **kwargs)

  if ordered:
    effect = debugging.DebugEffect.ORDERED_PRINT
  else:
    effect = debugging.DebugEffect.PRINT
  debugging.debug_callback(_breakpoint_callback, effect, *flat_args)
