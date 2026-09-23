  @property
  def physical_resource_axes(self) -> set[ResourceAxisName]:
    return set(self.physical_mesh.axis_names)
