  @property
  def global_shards(self) -> Sequence[Shard]:
    """Returns list of all `Shard`s of the Array across all devices.

    The result includes shards that are not addressable by the current process.
    If a `Shard` is not addressable, then its `data` will be `None`.
    """
    self._check_if_deleted()
    if self.is_fully_addressable:  # pylint: disable=using-constant-test
      return self.addressable_shards

    out = []
    device_id_to_buffer = {_get_device(a).id: a for a in self._arrays}
    for global_d in self.sharding.device_set:
      if device_id_to_buffer.get(global_d.id, None) is not None:
        array = device_id_to_buffer[global_d.id]
      else:
        array = None
      out.append(Shard(global_d, self.sharding, self.shape, array))
    return out
