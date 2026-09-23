class DShapedArray(UnshapedArray):
  __slots__ = ['shape']
  shape: tuple[AxisSize, ...]  # noqa: F821
  array_abstraction_level: int = 3

  def __init__(self, shape, dtype, weak_type=False):
    self.shape = shape
    self.dtype = dtype
    self.weak_type = weak_type

  ndim = property(lambda self: len(self.shape))
  size = property(lambda self:
                  0 if any(type(d) is int and d == 0 for d in self.shape)
                  else math.prod(self.shape))

  def str_short(self, short_dtypes=False) -> str:
    del short_dtypes  # ignored
    shape = f'{",".join(str(d) for d in self.shape)}' if self.shape else ''
    dtype = _short_dtype_name(self.dtype)
    return f'{dtype}[{shape}]'
  __str__ = __repr__ = str_short

  def update(self, shape=None, dtype=None, weak_type=None):
    if shape is None:
      shape = self.shape
    if dtype is None:
      dtype = self.dtype
    if weak_type is None:
      weak_type = self.weak_type
    return DShapedArray(shape, dtype, weak_type)

  def _len(self, tracer):
    return self.shape[0]

  def __eq__(self, other):
    return (type(self) is type(other)
            and self.dtype == other.dtype and self.shape == other.shape
            and self.weak_type == other.weak_type)

  def __hash__(self):
    return hash((self.shape, self.dtype, self.weak_type))

  def join(self, other):
    if (definitely_equal_shape(self.shape, other.shape) and
        self.dtype == other.dtype):
      weak_type = self.weak_type and other.weak_type
      return self.update(weak_type=weak_type)
    elif self.dtype == other.dtype:
      return UnshapedArray(self.dtype)
    else:
      raise TypeError(self, other)

  def at_least_vspace(self):
    return DShapedArray(self.shape, primal_dtype_to_tangent_dtype(self.dtype),
                        self.weak_type)
