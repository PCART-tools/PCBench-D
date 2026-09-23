def _axis_index_bind(*, axis_name):
  def name_idx(name):
    frame = core.axis_frame(name)
    dynamic = core.thread_local_state.trace_state.trace_stack.dynamic
    if (frame.main_trace is None or dynamic.level > frame.main_trace.level):
      return core.Primitive.bind(axis_index_p, axis_name=name)
    else:
      trace = frame.main_trace.with_cur_sublevel()
      return trace.process_axis_index(frame)

  if not isinstance(axis_name, (tuple, list)):
    return name_idx(axis_name)
  else:
    inner_size = 1
    index = 0
    for name in reversed(axis_name):
      index += name_idx(name) * inner_size
      inner_size *= psum(1, name)
    return index
