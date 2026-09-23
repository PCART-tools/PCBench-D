class ResourceEnv(NamedTuple):
  physical_mesh: Mesh
  loops: tuple[Loop, ...]

  def with_mesh(self, mesh: Mesh):
    overlap = set(mesh.axis_names) & (self.resource_axes - set(self.physical_mesh.axis_names))
    if overlap:
      raise ValueError(f"Cannot update the mesh of the current resource "
                       f"environment. The new mesh shadows already defined axes "
                       f"{show_axes(overlap)}")
    return self._replace(physical_mesh=mesh)

  def with_extra_loop(self, loop: Loop):
    if loop.name in self.resource_axes:
      raise ValueError(f"Cannot extend the resource environment with loop named "
                       f"`{loop.name}`. An axis of this name is already defined!")
    return self._replace(loops=self.loops + (loop,))

  @property
  def physical_resource_axes(self) -> set[ResourceAxisName]:
    return set(self.physical_mesh.axis_names)

  @property
  def loop_resource_axes(self) -> set[ResourceAxisName]:
    return {loop.name for loop in self.loops}

  @property
  def resource_axes(self) -> set[ResourceAxisName]:
    return self.physical_resource_axes | self.loop_resource_axes

  @property
  def shape(self):
    shape = self.physical_mesh.shape
    shape.update(self.loops)
    return shape

  @property
  def local_shape(self):
    shape = self.physical_mesh.local_mesh.shape
    shape.update(self.loops)
    return shape

  def __repr__(self):
    mesh_repr = ", ".join(
        f"'{k}': {v}" for k, v in self.physical_mesh.shape.items())
    return f"ResourceEnv(mesh=Mesh({mesh_repr}), {self.loops!r})"
