  @property
  def shape(self):
    shape = self.physical_mesh.shape
    shape.update(self.loops)
    return shape
