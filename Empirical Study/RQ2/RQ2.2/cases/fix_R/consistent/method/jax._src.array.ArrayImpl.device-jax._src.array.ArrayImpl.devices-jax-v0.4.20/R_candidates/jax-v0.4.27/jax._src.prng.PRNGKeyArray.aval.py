  @property
  def aval(self):
    return keys_shaped_array(self._impl, self.shape)
