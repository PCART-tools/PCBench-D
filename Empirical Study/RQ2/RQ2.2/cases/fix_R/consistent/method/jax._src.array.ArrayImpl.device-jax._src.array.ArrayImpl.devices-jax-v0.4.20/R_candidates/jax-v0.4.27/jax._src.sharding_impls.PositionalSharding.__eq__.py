  def __eq__(self, other) -> bool:
    if not isinstance(other, PositionalSharding):
      return False
    if self is other:
      return True
    all_ids_equal = np.array_equal(self._ids,other._ids)
    mem_kind_equal = self.memory_kind == other.memory_kind
    if self._devices is other._devices and mem_kind_equal and all_ids_equal:
      return True
    return (mem_kind_equal and all_ids_equal and
            self._internal_device_list == other._internal_device_list)
