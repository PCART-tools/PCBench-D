  def instantiate_const(self, val):
    if (isinstance(val, Tracer) and val._trace.main is self.main
        and val._trace.sublevel == self.sublevel):
      return val
    else:
      return self.new_const(val)
