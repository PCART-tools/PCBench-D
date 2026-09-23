  def join(self, other) -> AbstractValue:
    if self == other:
      return self
    elif self.shape == other.shape and self.dtype == other.dtype:
      weak_type = self.weak_type and other.weak_type
      named_shape = join_named_shapes(self.named_shape, other.named_shape)
      return ShapedArray(
          self.shape, self.dtype, weak_type=weak_type, named_shape=named_shape)
    elif self.dtype == other.dtype:
      return UnshapedArray(self.dtype,
                           weak_type=self.weak_type and other.weak_type)
    else:
      raise TypeError(self, other)
