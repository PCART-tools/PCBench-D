  @functools.cached_property
  def device_set(self) -> set[xc.Device]:
    return set(self._devices)
