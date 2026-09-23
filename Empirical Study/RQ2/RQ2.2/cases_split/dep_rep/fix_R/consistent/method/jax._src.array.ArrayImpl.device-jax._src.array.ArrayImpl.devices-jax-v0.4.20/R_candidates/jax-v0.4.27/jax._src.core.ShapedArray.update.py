  def update(self, shape=None, dtype=None, weak_type=None, named_shape=None):
    if shape is None:
      shape = self.shape
    if dtype is None:
      dtype = self.dtype
    if weak_type is None:
      weak_type = self.weak_type
    if named_shape is None:
      named_shape = self.named_shape
    return ShapedArray(shape, dtype, weak_type, named_shape)
