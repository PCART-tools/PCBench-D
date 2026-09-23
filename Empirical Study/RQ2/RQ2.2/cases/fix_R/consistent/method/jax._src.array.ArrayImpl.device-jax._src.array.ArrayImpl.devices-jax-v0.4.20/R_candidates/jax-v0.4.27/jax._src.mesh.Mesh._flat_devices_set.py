  @functools.cached_property
  def _flat_devices_set(self):
    return set(self.devices.flat)
