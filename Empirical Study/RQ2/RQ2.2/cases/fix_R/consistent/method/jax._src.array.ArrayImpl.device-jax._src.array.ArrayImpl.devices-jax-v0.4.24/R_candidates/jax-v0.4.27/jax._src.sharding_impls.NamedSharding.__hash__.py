  def __hash__(self):
    if not hasattr(self, '_hash'):
      self._hash = hash(
          (self.mesh, self.memory_kind, self._parsed_pspec, self._manual_axes))
    return self._hash
