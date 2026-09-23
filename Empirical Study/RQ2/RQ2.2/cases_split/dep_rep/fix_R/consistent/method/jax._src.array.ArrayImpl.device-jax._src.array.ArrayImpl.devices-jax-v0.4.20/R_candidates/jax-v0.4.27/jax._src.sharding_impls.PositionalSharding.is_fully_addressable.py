  @functools.cached_property
  def is_fully_addressable(self) -> bool:
    return self._internal_device_list.is_fully_addressable
