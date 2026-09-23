  @functools.cached_property
  def local_devices(self):
    return [d for d in self.devices.flat
            if d.process_index == d.client.process_index()]
