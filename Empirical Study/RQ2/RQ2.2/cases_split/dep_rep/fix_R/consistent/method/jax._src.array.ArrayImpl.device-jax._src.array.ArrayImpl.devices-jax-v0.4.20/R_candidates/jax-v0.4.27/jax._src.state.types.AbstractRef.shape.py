  @property
  def shape(self):
    if not isinstance(self.inner_aval, core.ShapedArray):
      raise AttributeError(f"`Ref{{{self.inner_aval.str_short()}}} has no `shape`.")
    return self.inner_aval.shape
