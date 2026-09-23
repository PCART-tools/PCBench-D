def _forward_to_value(self, fun, ignored_tracer, *args):
  return fun(self.val, *args)
