  def update(self, dtype=None, weak_type=None):
    if dtype is None:
      dtype = self.dtype
    if weak_type is None:
      weak_type = self.weak_type
    return UnshapedArray(dtype, weak_type)
