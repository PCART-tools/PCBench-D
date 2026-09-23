  def __eq__(self, other):
    if not isinstance(other, NamedSharding):
      return False
    if self is other:
      return True
    if (self._parsed_pspec != other._parsed_pspec
        or self.memory_kind != other.memory_kind
        or self._manual_axes != other._manual_axes):
      return False
    return self.mesh is other.mesh or self.mesh == other.mesh
