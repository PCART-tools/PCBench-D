  @functools.cached_property
  def _local_devices_set(self):
    return set(self.local_devices)
