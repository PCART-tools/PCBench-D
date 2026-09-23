  def addressable_devices_indices_map(
      self, global_shape: Shape) -> Mapping[Device, Index | None]:
    """A mapping from addressable devices to the slice of array data each contains.

    ``addressable_devices_indices_map`` contains that part of
    ``device_indices_map`` that applies to the addressable devices.
    """
    return _addressable_devices_indices_map(self, global_shape)
