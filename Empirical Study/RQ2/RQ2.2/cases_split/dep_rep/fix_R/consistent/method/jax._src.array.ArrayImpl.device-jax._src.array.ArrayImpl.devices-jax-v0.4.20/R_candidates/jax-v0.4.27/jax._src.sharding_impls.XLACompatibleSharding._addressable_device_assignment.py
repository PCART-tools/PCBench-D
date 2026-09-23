  @functools.cached_property
  def _addressable_device_assignment(self) -> XLADeviceAssignment:
    if self.is_fully_addressable:
      return self._device_assignment
    if hasattr(self, '_internal_device_list'):
      return tuple(self._internal_device_list.addressable_device_list)
    return tuple(d for d in self._device_assignment
                 if d.process_index == d.client.process_index())
