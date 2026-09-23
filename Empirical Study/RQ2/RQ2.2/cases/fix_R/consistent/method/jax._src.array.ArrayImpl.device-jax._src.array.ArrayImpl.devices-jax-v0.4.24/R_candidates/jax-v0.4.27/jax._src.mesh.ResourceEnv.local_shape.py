  @property
  def local_shape(self):
    shape = self.physical_mesh.local_mesh.shape
    shape.update(self.loops)
    return shape
