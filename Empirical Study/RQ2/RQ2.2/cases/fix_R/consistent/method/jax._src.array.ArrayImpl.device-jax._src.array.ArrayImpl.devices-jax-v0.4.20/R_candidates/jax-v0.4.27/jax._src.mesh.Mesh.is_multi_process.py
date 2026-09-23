  @functools.cached_property
  def is_multi_process(self):
    return self.devices.size != len(self.local_devices)
