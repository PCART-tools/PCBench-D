def _forward_method_to_aval(name):
  def meth(self, *args, **kwargs):
    return getattr(self.aval, name).fun(self, *args, **kwargs)
  return meth
