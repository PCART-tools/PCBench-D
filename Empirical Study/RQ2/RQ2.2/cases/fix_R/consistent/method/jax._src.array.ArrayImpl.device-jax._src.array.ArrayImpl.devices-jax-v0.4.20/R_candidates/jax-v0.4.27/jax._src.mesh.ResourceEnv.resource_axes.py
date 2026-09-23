  @property
  def resource_axes(self) -> set[ResourceAxisName]:
    return self.physical_resource_axes | self.loop_resource_axes
