  def __len__(self):
    """Number of rotations contained in this object."""
    if self.single:
      raise TypeError('Single rotation has no len().')
    else:
      return self.quat.shape[0]
