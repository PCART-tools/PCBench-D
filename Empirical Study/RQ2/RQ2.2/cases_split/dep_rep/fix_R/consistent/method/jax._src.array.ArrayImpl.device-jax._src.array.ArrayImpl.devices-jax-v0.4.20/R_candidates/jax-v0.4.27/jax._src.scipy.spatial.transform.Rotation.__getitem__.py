  def __getitem__(self, indexer):
    """Extract rotation(s) at given index(es) from object."""
    if self.single:
      raise TypeError("Single rotation is not subscriptable.")
    return Rotation(self.quat[indexer])
