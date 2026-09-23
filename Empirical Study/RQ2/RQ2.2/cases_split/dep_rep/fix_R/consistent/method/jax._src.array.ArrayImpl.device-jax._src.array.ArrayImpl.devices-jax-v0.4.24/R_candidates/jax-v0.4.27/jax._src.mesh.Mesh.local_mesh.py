  @property
  def local_mesh(self):
    return self._local_mesh(xb.process_index())
