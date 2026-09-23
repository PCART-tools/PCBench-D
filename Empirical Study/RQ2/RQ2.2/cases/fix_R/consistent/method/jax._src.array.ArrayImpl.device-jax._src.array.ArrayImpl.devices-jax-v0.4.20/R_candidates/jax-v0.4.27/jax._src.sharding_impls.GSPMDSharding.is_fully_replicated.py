  @functools.cached_property
  def is_fully_replicated(self) -> bool:
    return is_op_sharding_replicated(self._hlo_sharding)
