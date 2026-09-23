  @property
  def device_set(self) -> set[Device]:
    return self.mesh._flat_devices_set
