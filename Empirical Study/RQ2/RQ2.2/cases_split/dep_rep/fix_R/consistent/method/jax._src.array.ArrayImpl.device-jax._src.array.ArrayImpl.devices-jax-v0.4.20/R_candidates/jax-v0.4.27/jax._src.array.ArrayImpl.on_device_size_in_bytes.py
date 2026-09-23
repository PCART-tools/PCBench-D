  @use_cpp_method()
  def on_device_size_in_bytes(self):
    """Returns the total global on-device size of the array in bytes."""
    arr = self._arrays[0]
    per_shard_size = arr.on_device_size_in_bytes()  # type: ignore
    return per_shard_size * len(self.sharding.device_set)
