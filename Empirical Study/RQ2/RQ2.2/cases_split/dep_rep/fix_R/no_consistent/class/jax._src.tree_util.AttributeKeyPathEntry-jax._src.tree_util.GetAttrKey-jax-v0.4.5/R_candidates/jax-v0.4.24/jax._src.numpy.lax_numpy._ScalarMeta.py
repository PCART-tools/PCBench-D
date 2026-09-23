class _ScalarMeta(type):
  dtype: np.dtype

  def __hash__(self) -> int:
    return hash(self.dtype.type)

  def __eq__(self, other: Any) -> bool:
    return id(self) == id(other) or self.dtype.type == other

  def __ne__(self, other: Any) -> bool:
    return not (self == other)

  def __call__(self, x: Any) -> Array:
    return asarray(x, dtype=self.dtype)

  def __instancecheck__(self, instance: Any) -> bool:
    return isinstance(instance, self.dtype.type)
