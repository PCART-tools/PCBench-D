  @functools.cached_property
  def replica_id(self) -> int:
    return device_replica_id_map(self._sharding, self._global_shape)[self.device]
