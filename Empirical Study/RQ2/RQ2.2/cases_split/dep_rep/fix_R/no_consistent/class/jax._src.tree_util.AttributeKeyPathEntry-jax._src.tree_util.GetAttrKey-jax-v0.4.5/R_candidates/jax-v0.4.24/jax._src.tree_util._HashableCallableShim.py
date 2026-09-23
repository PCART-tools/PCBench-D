class _HashableCallableShim:
  """Object that delegates __call__, __hash__, and __eq__ to another object."""

  def __init__(self, fun):
    self.fun = fun

  def __call__(self, *args, **kw):
    return self.fun(*args, **kw)

  def __hash__(self):
    return hash(self.fun)

  def __eq__(self, other):
    if isinstance(other, _HashableCallableShim):
      return self.fun == other.fun
    return self.fun == other

  def __repr__(self):
    return f'_HashableCallableShim({self.fun!r})'
