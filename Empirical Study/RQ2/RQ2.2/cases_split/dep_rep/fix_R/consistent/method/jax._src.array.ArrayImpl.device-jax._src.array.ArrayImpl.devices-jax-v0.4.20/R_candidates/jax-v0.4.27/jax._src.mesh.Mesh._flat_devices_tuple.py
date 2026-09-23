  @functools.cached_property
  def _flat_devices_tuple(self):
    return tuple(self.devices.flat)
