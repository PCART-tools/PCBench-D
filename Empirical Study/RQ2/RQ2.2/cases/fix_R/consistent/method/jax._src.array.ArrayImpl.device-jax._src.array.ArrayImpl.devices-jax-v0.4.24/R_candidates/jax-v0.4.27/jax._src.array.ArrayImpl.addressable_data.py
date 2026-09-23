  def addressable_data(self, index: int) -> ArrayImpl:
    self._check_if_deleted()
    if self.is_fully_replicated:
      return self._fully_replicated_shard()
    return self._arrays[index]
