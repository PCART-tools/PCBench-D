  def block_until_ready(self):
    _ = self._data.block_until_ready()
    return self
