def _add_args(f, extra_args):
  return _add_args_(f, tuple(Unhashable(arg) for arg in extra_args))
