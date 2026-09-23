  def __reduce__(self):
    return (type(self), (self.mesh, self.spec),
            {'memory_kind': self.memory_kind,
             '_manual_axes': self._manual_axes})
