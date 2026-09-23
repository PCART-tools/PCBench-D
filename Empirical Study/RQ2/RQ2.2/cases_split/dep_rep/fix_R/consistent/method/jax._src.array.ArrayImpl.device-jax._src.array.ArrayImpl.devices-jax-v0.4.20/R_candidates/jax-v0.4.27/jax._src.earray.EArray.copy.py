  def copy(self):
    return EArray(self.aval, self._data.copy())
