  @property
  def dtype(self):
    if not isinstance(self.inner_aval, core.UnshapedArray):
      raise AttributeError(f"`Ref{{{self.inner_aval.str_short()}}} has no `dtype`.")
    return self.inner_aval.dtype
