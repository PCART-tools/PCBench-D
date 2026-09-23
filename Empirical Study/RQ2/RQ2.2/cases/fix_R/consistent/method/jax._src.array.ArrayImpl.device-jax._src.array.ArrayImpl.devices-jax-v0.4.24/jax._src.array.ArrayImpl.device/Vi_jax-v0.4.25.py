  def device(self) -> Device:
    if deprecations.is_accelerated(__name__, "device-method"):
      raise NotImplementedError("arr.device() is deprecated. Use arr.devices() instead.")
    else:
      warnings.warn("arr.device() is deprecated. Use arr.devices() instead.",
                    DeprecationWarning, stacklevel=2)
    self._check_if_deleted()
    device_set = self.sharding.device_set
    if len(device_set) == 1:
      single_device, = device_set
      return single_device
    raise ValueError('Length of devices is greater than 1. '
                     'Please use `.devices()`.')
