  @functools.cached_property
  def _device_assignment(self) -> XLADeviceAssignment:
    return tuple(self.devices.flat)
