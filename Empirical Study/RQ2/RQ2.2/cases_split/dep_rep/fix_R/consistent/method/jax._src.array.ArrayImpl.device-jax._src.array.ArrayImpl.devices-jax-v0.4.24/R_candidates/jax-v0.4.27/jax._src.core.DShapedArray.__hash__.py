  def __hash__(self):
    return hash((self.shape, self.dtype, self.weak_type))
