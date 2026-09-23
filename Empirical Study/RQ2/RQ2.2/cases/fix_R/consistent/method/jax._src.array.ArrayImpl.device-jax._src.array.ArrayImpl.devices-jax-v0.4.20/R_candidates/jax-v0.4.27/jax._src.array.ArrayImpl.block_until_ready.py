  @use_cpp_method()
  def block_until_ready(self):
    self._check_if_deleted()
    for db in self._arrays:
      db.block_until_ready()
    return self
