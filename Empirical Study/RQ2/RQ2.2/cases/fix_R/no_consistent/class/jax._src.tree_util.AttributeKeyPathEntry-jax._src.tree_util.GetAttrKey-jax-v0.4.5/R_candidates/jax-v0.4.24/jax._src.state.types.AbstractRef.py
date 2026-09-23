class AbstractRef(core.AbstractValue, Generic[Aval]):
  __slots__ = ["inner_aval"]

  def __init__(self, inner_aval: core.AbstractValue):
    self.inner_aval = inner_aval

  def update(self, inner_aval=None):
    if inner_aval is None:
      return AbstractRef(self.inner_aval)
    return AbstractRef(inner_aval)

  def join(self, other):
    assert isinstance(other, AbstractRef)
    return AbstractRef(self.inner_aval.join(other.inner_aval))

  ndim = property(lambda self: len(self.shape))
  size = property(lambda self: math.prod(self.shape))

  @property
  def shape(self):
    if not isinstance(self.inner_aval, core.ShapedArray):
      raise AttributeError(f"`Ref{{{self.inner_aval.str_short()}}} has no `shape`.")
    return self.inner_aval.shape

  @property
  def dtype(self):
    if not isinstance(self.inner_aval, core.UnshapedArray):
      raise AttributeError(f"`Ref{{{self.inner_aval.str_short()}}} has no `dtype`.")
    return self.inner_aval.dtype

  @core.aval_property
  def at(self):
    return RefIndexer(self)

  @core.aval_method
  @staticmethod
  def get(tracer, idx=()):
    from jax._src.state.primitives import ref_get  # pytype: disable=import-error
    return ref_get(tracer, idx)

  @core.aval_method
  @staticmethod
  def set(tracer, value, idx=()):
    from jax._src.state.primitives import ref_set  # pytype: disable=import-error
    return ref_set(tracer, idx, value)

  def _getitem(self, tracer, idx) -> Array:
    from jax._src.state.primitives import ref_get  # pytype: disable=import-error
    return ref_get(tracer, idx)

  def _setitem(self, tracer, idx, value) -> None:
    from jax._src.state.primitives import ref_set  # pytype: disable=import-error
    return ref_set(tracer, idx, value)

  def __repr__(self) -> str:
    return f'Ref{{{self.inner_aval.str_short()}}}'

  def at_least_vspace(self):
    return AbstractRef(self.inner_aval.at_least_vspace())

  def __eq__(self, other):
    return (type(self) is type(other) and self.inner_aval == other.inner_aval)

  def __hash__(self):
    return hash((self.__class__, self.inner_aval))
