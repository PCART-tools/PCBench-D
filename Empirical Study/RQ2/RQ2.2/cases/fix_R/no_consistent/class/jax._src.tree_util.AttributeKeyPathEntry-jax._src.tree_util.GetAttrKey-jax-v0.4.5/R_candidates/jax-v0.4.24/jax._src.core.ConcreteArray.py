class ConcreteArray(ShapedArray):
  __slots__ = ['val']
  array_abstraction_level = 0

  def __init__(self, dtype, val, weak_type=None):
    super().__init__(
        np.shape(val), dtype,
        weak_type=dtypes.is_weakly_typed(val) if weak_type is None else weak_type)
    dtypes.check_valid_dtype(self.dtype)
    # Note: canonicalized self.dtype doesn't necessarily match self.val
    assert self.dtype == dtypes.canonicalize_dtype(np.result_type(val)), (val, dtype)
    self.val = val

  def update(self, dtype=None, val=None, weak_type=None):
    dtype = self.dtype if dtype is None else dtype
    val = self.val if val is None else val
    weak_type = self.weak_type if weak_type is None else weak_type
    return ConcreteArray(dtype, val, weak_type)

  def __eq__(self, other):
    if (type(self) is type(other) and self.dtype == other.dtype
        and self.shape == other.shape and self.weak_type == other.weak_type):
      with eval_context():  # in case self.val is an Array
        return (self.val == other.val).all()
    else:
      return False

  def __hash__(self):
    return id(self.val)

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

  def str_short(self, short_dtypes=False) -> str:
    dt_str =  _short_dtype_name(self.dtype) if short_dtypes else self.dtype.name
    return f'{self.val}, dtype={dt_str}'

  _bool    = partialmethod(_forward_to_value, bool)
  _int     = partialmethod(_forward_to_value, int)
  _hex     = partialmethod(_forward_to_value, hex)
  _oct     = partialmethod(_forward_to_value, oct)
  _index   = partialmethod(_forward_to_value, operator.index)

  _float   = concretization_function_error(float, True)
  _complex = concretization_function_error(complex, True)
