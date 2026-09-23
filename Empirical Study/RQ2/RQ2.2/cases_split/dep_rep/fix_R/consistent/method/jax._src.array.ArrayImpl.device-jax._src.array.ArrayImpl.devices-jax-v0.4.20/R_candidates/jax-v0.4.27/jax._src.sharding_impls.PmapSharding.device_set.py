  @functools.cached_property
  def device_set(self) -> set[Device]:
    return set(self.devices.flat)
