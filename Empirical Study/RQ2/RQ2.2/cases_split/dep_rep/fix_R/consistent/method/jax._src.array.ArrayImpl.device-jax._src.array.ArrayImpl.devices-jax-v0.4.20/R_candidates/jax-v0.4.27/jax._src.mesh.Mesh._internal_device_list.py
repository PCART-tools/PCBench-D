  @functools.cached_property
  def _internal_device_list(self):
    return xc.DeviceList(self._flat_devices_tuple)
