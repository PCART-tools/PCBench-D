  def newvar(self, aval):
    if isinstance(aval, DShapedArray):
      # this aval may have tracers in it, so we replace those with variables
      new_shape = [self.tracer_to_var[id(d)] if isinstance(d, Tracer) else d
                   for d in aval.shape]
      aval = aval.update(shape=tuple(new_shape))
    return self.gensym(aval)
