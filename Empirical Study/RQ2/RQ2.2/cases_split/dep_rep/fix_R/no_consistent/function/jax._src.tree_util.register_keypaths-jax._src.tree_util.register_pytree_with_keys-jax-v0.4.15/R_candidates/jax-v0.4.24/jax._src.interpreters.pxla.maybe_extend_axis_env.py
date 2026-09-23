@contextmanager
def maybe_extend_axis_env(*args, **kwargs):
  with core.extend_axis_env(*args, **kwargs):
    yield
