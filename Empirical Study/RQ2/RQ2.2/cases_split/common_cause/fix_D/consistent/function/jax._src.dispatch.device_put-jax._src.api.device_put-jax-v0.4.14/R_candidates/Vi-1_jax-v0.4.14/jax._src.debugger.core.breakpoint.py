def breakpoint(*, backend: str | None = None, filter_frames: bool = True,
               num_frames: int | None = None, ordered: bool = False,
               **kwargs):  # pylint: disable=redefined-builtin
  """Enters a breakpoint at a point in a program.

  Args:
    backend: The debugger backend to use. By default, picks the highest priority
      debugger and in the absence of other registered debuggers, falls back to
      the CLI debugger.
    filter_frames: Whether or not to filter out JAX-internal stack frames from
      the traceback. Since some libraries, like Flax, also make user of JAX's
      stack frame filtering system, this option can also affect whether stack
      frames from libraries are filtered.
    num_frames: The number of frames above the current stack frame to make
      available for inspection in the interactive debugger.
    ordered: A keyword only argument used to indicate whether or not the
      staged out computation will enforce ordering of this ``debug_print``
      with respect to other ordered ``debug_print`` calls.

  Returns:
    None.
  """
  frame_infos = inspect.stack()
  # Throw out first frame corresponding to this function
  frame_infos = frame_infos[1:]
  if num_frames is not None:
    frame_infos = frame_infos[:num_frames]
  # Filter out internal frames
  if filter_frames:
    frames = [
        DebuggerFrame.from_frameinfo(frame_info)
        for frame_info in frame_infos
        if traceback_util.include_frame(frame_info.frame)
    ]
  else:
    frames = [
        DebuggerFrame.from_frameinfo(frame_info)
        for frame_info in frame_infos
    ]
  flat_args, frames_tree = tree_util.tree_flatten(frames)

  def _breakpoint_callback(*flat_args):
    frames = tree_util.tree_unflatten(frames_tree, flat_args)
    thread_id = None
    if threading.current_thread() is not threading.main_thread():
      thread_id = threading.get_ident()
    debugger = get_debugger(backend=backend)
    # Lock here because this could be called from multiple threads at the same
    # time.
    with debug_lock:
      debugger(frames, thread_id, **kwargs)

  debugging.debug_callback(_breakpoint_callback, *flat_args, ordered=ordered)
