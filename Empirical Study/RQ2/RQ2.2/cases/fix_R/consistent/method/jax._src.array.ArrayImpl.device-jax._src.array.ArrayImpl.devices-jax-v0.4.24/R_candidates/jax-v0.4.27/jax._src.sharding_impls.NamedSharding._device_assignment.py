  @property
  def _device_assignment(self) -> XLADeviceAssignment:
    return self.mesh._flat_devices_tuple
