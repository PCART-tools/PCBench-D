  def copy(self):
    out = self.__class__(self._impl, self._base_array.copy())
    out._consumed = self._consumed  # TODO(jakevdp): is this correct?
    return out
