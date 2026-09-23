class _ScalarMeta(type):
  def __hash__(self):
    return hash(self.dtype.type)

  def __eq__(self, other):
    return id(self) == id(other) or self.dtype.type == other

  def __ne__(self, other):
    return not (self == other)

  def __call__(self, x):
    return asarray(x, dtype=self.dtype)

  def __instancecheck__(self, instance):
    return isinstance(instance, self.dtype.type)
