def axis_frame(axis_name):
  frames = thread_local_state.trace_state.axis_env
  for frame in reversed(frames):
    if frame.name == axis_name:
      return frame
  named_axes = [frame.name for frame in reversed(frames)
                if not isinstance(frame.name, _TempAxisName)]
  raise NameError(
      f'unbound axis name: {axis_name}. The following axis names (e.g. defined '
      f'by pmap) are available to collective operations: {named_axes}')
