  def update(self, shape=None, dtype=None, weak_type=None):
    if shape is None:
      shape = self.shape
    if dtype is None:
      dtype = self.dtype
    if weak_type is None:
      weak_type = self.weak_type
    return DShapedArray(shape, dtype, weak_type)
