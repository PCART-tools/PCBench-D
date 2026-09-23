  def block_until_ready(self):
    _ = self._base_array.block_until_ready()
    return self
