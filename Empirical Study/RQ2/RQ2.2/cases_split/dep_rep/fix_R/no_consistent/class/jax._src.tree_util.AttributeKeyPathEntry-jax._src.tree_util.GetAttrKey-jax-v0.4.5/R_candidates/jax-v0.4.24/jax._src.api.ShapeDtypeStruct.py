class ShapeDtypeStruct:
  """A container for the shape, dtype, and other static attributes of an array.

  ``ShapeDtypeStruct`` is often used in conjunction with :func:`jax.eval_shape`.

  Args:
    shape: a sequence of integers representing an array shape
    dtype: a dtype-like object
    named_shape: (optional) a dictionary representing a named shape
    sharding: (optional) a :class:`jax.Sharding` object
  """
  __slots__ = ["shape", "dtype", "named_shape", "sharding"]
  def __init__(self, shape, dtype, named_shape=None, sharding=None):
    self.shape = tuple(shape)
    if dtype is None:
      raise ValueError("ShapeDtypeStruct: dtype must be specified.")
    self.dtype = dtype if dtypes.issubdtype(dtype, dtypes.extended) else np.dtype(dtype)
    if sharding is not None and not isinstance(sharding, Sharding):
      raise ValueError(
          "sharding should be an instance of `jax.sharding.Sharding`. "
          f"Got {sharding} of type {type(sharding)}.")
    self.sharding = sharding
    self.named_shape = {} if named_shape is None else dict(named_shape)

  size = property(lambda self: math.prod(self.shape))
  ndim = property(lambda self: len(self.shape))

  def __len__(self):
    try:
      return self.shape[0]
    except IndexError as e:
      raise TypeError("len() of unsized object") from e  # same as numpy error

  def __repr__(self):
    ns = f", named_shape={self.named_shape}" if self.named_shape else ""
    sh = f", sharding={self.sharding}" if self.sharding is not None else ""
    return (f"{type(self).__name__}(shape={self.shape}, "
            f"dtype={self.dtype.name}{ns}{sh})")

  __str__ = __repr__

  def __eq__(self, other):
    if not isinstance(other, ShapeDtypeStruct):
      return False
    else:
      return ((other.shape, other.dtype, other.named_shape, other.sharding) ==
              (self.shape, self.dtype, self.named_shape, self.sharding))

  def __hash__(self):
    # TODO(frostig): avoid the conversion from dict by addressing
    # https://github.com/google/jax/issues/8182
    named = frozenset(self.named_shape.items())
    return hash((self.shape, self.dtype, named, self.sharding))
