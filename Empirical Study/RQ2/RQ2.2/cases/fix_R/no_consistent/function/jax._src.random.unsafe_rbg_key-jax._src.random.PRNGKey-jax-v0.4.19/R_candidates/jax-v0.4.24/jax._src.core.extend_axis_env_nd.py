@contextmanager
def extend_axis_env_nd(axes: Iterable[tuple[AxisName, int]], tag: Any = None):
  frames = [AxisEnvFrame(axis_name, size, tag) for axis_name, size in axes]
  ts = thread_local_state.trace_state
  ts.axis_env.extend(frames)
  config.update_thread_local_jit_state(
      axis_env_state=tuple(f for f in ts.axis_env
                           if f.name is not no_axis_name))
  try:
    yield
  finally:
    for _ in frames: ts.axis_env.pop()
    config.update_thread_local_jit_state(
        axis_env_state=tuple(f for f in ts.axis_env
                             if f.name is not no_axis_name))
