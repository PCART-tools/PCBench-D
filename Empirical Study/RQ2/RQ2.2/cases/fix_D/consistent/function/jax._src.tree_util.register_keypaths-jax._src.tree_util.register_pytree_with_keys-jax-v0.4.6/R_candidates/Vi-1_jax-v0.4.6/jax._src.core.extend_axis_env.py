@contextmanager
def extend_axis_env(axis_name: AxisName, size: int, tag: Any):
  frame = AxisEnvFrame(axis_name, size, tag)
  ts = thread_local_state.trace_state
  ts.axis_env.append(frame)
  jax_config.update_thread_local_jit_state(
      axis_env_state=tuple(f for f in ts.axis_env
                           if f.name is not no_axis_name))
  try:
    yield
  finally:
    ts.axis_env.pop()
    jax_config.update_thread_local_jit_state(
        axis_env_state=tuple(f for f in ts.axis_env
                             if f.name is not no_axis_name))
