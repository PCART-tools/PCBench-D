  def __eq__(self, other):
    if not isinstance(other, Mesh):
      return False
    # This is a performance optimization. Comparing thousands of devices
    # can be expensive.
    if id(self) == id(other):
      return True
    return (self.axis_names == other.axis_names and
            self.devices.shape == other.devices.shape and
            self._internal_device_list == other._internal_device_list)
