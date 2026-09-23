class ShapedArray(UnshapedArray):
  __slots__ = ['shape', 'named_shape']
  array_abstraction_level = 2

  def __init__(self, shape, dtype, weak_type=False, named_shape=None):
    self.shape = canonicalize_shape(shape)
    self.dtype = _dtype_object(dtype)
    self.weak_type = weak_type
    self.named_shape = {} if named_shape is None else dict(named_shape)

  def update(self, shape=None, dtype=None, weak_type=None, named_shape=None):
    if shape is None:
      shape = self.shape
    if dtype is None:
      dtype = self.dtype
    if weak_type is None:
      weak_type = self.weak_type
    if named_shape is None:
      named_shape = self.named_shape
    return ShapedArray(shape, dtype, weak_type, named_shape)

  ndim = property(lambda self: len(self.shape))
  size = property(lambda self:
                  0 if any(type(d) is int and d == 0 for d in self.shape)
                  else math.prod(self.shape))

  broadcast: ClassVar[aval_method | None] = None
  transpose: ClassVar[aval_method | None] = None
  reshape: ClassVar[aval_method | None] = None
  _iter: ClassVar[staticmethod | None] = None

  def __eq__(self, other):
    return (type(self) is type(other)
            and self.dtype == other.dtype and self.shape == other.shape
            and self.weak_type == other.weak_type
            and self.named_shape == other.named_shape)

  def __hash__(self):
    # can use hash(self.dtype) and rely on the fact that numpy reuses base dtype
    # objects, e.g. `np.zeros(3).dtype is np.zeros(4).dtype`, or we can use
    # the unique character code via hash(self.dtype.char)
    return hash((self.shape, self.dtype, self.weak_type,
                 tuple(self.named_shape.items())))

  def at_least_vspace(self):
    return ShapedArray(self.shape, primal_dtype_to_tangent_dtype(self.dtype),
                       self.weak_type, self.named_shape)

  def join(self, other):
    if definitely_equal_shape(self.shape, other.shape) and self.dtype == other.dtype:
      weak_type = self.weak_type and other.weak_type
      named_shape = join_named_shapes(self.named_shape, other.named_shape)
      return self.update(weak_type=weak_type, named_shape=named_shape)
    elif self.dtype == other.dtype:
      return UnshapedArray(self.dtype)
    else:
      raise TypeError(self, other)

  def str_short(self, short_dtypes=False):
    dt_str =  _short_dtype_name(self.dtype) if short_dtypes else self.dtype.name
    shapestr = ','.join(map(str, self.shape))
    if self.named_shape:
      named_shapestr = ','.join(f'{k}:{v}' for k, v in self.named_shape.items())
      return f'{dt_str}[{shapestr};{named_shapestr}]'
    else:
      return f'{dt_str}[{shapestr}]'

  def strip_named_shape(self):
    return self.update(named_shape={})

  def _len(self, ignored_tracer):
    try:
      return self.shape[0]
    except IndexError as err:
      raise TypeError("len() of unsized object") from err  # same as numpy error
