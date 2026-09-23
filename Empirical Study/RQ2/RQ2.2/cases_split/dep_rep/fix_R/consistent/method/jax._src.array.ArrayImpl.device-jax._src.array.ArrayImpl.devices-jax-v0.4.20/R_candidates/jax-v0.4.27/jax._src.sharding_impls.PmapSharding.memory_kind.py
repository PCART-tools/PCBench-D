  @property
  def memory_kind(self) -> str | None:
    try:
      return self._internal_device_list.default_memory_kind  # type: ignore
    except:
      return None
