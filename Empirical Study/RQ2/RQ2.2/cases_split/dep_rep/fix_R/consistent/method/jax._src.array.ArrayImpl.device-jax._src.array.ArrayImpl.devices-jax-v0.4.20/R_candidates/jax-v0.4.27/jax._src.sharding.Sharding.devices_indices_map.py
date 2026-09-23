  def devices_indices_map(
      self, global_shape: Shape) -> Mapping[Device, Index | None]:
    """Returns a mapping from devices to the array slices each contains.

    The mapping includes all global devices, i.e., including
    non-addressable devices from other processes.
    """
    raise NotImplementedError('Subclasses should implement this method.')
