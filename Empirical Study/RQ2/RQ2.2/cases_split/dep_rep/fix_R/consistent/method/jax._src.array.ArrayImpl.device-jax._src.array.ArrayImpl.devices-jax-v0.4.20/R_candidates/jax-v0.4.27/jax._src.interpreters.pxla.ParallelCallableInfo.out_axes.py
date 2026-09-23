  @cached_property
  def out_axes(self):
    return self.out_axes_thunk()
