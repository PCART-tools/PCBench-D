class ShapeDtypeStruct:
  __slots__ = ["shape", "dtype", "named_shape"]
  def __init__(self, shape, dtype, named_shape=None):
    self.shape = shape
    self.dtype = np.dtype(dtype)
    self.named_shape = {} if named_shape is None else dict(named_shape)

  size = property(lambda self: prod(self.shape))
  ndim = property(lambda self: len(self.shape))

  def __len__(self):
    try:
      return self.shape[0]
    except IndexError as e:
      raise TypeError("len() of unsized object") from e # same as numpy error

  def __repr__(self):
    ns = f", named_shape={self.named_shape}" if self.named_shape else ""
    return f"{type(self).__name__}(shape={self.shape}, dtype={self.dtype.name}{ns})"

  __str__ = __repr__

  def __eq__(self, other):
    if not isinstance(other, ShapeDtypeStruct):
      return False
    else:
      return (other.shape, other.dtype, other.named_shape) == (
          self.shape, self.dtype, self.named_shape)

  def __hash__(self):
    # TODO(frostig): avoid the conversion from dict by addressing
    # https://github.com/google/jax/issues/8182
    named = frozenset(self.named_shape.items())
    return hash((self.shape, self.dtype, named))
