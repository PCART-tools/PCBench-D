class KeyTy(dtypes.ExtendedDType):
  _impl: PRNGImpl  # TODO(mattjj,frostig): protocol really
  _rules = KeyTyRules
  type = dtypes.prng_key

  def __init__(self, impl):
    self._impl = impl

  @property
  def name(self) -> str:
    return f'key<{self._impl.tag}>'

  @property
  def itemsize(self) -> int:
    return math.prod(self._impl.key_shape) * np.dtype('uint32').itemsize

  def __repr__(self) -> str:
    return self.name

  def __eq__(self, other):
    return type(other) is KeyTy and self._impl == other._impl

  def __hash__(self) -> int:
    return hash((self.__class__, self._impl))
