  def __eq__(self, other):
    if isinstance(other, _HashableCallableShim):
      return self.fun == other.fun
    return self.fun == other
