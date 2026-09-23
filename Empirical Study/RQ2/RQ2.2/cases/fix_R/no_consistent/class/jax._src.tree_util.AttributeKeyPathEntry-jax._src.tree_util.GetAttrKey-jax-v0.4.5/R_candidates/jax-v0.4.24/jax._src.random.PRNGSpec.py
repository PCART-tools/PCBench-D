class PRNGSpec:
  """Specifies a PRNG key implementation."""

  __slots__ = ['_impl']
  _impl: PRNGImpl

  def __init__(self, impl):
    self._impl = impl

  def __str__(self)  -> str: return str(self._impl)
  def __hash__(self) -> int: return hash(self._impl)

  def __eq__(self, other) -> bool:
    return self._impl == other._impl
