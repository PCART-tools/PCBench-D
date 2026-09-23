  def __hash__(self):
    if not hasattr(self, '_hash'):
      self._hash = hash(
          (self.axis_names, self._internal_device_list, self.devices.shape))
    return self._hash
