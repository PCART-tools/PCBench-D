  def update(self, dtype=None, val=None, weak_type=None):
    dtype = self.dtype if dtype is None else dtype
    val = self.val if val is None else val
    weak_type = self.weak_type if weak_type is None else weak_type
    return ConcreteArray(dtype, val, weak_type)
