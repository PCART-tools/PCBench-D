  def join(self, other):
    if definitely_equal_shape(self.shape, other.shape) and self.dtype == other.dtype:
      weak_type = self.weak_type and other.weak_type
      named_shape = join_named_shapes(self.named_shape, other.named_shape)
      return self.update(weak_type=weak_type, named_shape=named_shape)
    elif self.dtype == other.dtype:
      return UnshapedArray(self.dtype)
    else:
      raise TypeError(self, other)
