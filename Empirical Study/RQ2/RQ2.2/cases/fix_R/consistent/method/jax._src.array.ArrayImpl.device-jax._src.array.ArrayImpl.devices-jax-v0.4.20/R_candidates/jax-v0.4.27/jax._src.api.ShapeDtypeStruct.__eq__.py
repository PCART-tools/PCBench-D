  def __eq__(self, other):
    if not isinstance(other, ShapeDtypeStruct):
      return False
    else:
      return ((other.shape, other.dtype, other.named_shape, other.sharding, other.layout) ==
              (self.shape, self.dtype, self.named_shape, self.sharding, self.layout))
