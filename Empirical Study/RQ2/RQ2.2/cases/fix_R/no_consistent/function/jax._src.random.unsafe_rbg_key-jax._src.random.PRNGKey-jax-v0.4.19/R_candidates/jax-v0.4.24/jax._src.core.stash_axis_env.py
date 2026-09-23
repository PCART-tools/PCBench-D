@contextmanager
def stash_axis_env():
  "Promise that a function or with-suite does not depend implicitly on axis env"
  # If the promise is broken, then a NameError about an unbound axis name will
  # be raised.
  ts = thread_local_state.trace_state
  prev_axis_env, ts.axis_env = ts.axis_env, []
  config.update_thread_local_jit_state(axis_env_state=())
  try:
    yield
  finally:
    ts.axis_env = prev_axis_env
    config.update_thread_local_jit_state(
        axis_env_state=tuple(f for f in ts.axis_env
                             if f.name is not no_axis_name))
