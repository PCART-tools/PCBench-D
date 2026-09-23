  @property
  def loop_resource_axes(self) -> set[ResourceAxisName]:
    return {loop.name for loop in self.loops}
