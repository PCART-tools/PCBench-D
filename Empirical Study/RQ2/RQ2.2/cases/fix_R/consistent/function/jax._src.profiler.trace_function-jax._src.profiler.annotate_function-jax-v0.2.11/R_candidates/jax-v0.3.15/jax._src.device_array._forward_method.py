def _forward_method(attrname, self, fun, *args):
  return fun(getattr(self, attrname), *args)
