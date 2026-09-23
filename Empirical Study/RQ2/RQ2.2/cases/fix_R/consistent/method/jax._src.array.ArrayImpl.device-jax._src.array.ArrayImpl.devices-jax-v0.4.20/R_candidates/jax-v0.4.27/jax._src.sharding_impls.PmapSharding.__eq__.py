  def __eq__(self, other):
    if not isinstance(other, PmapSharding):
      return False
    if self is other:
      return True
    return (self.sharding_spec == other.sharding_spec and
            self.devices.shape == other.devices.shape and
            self._internal_device_list == other._internal_device_list)  # type: ignore
