  def __eq__(self, other):
    if not isinstance(other, GSPMDSharding):
      return False
    if self is other:
      return True
    return (are_op_shardings_equal(self._hlo_sharding, other._hlo_sharding)
            and self.memory_kind == other.memory_kind
            and self._internal_device_list == other._internal_device_list)  # type: ignore
