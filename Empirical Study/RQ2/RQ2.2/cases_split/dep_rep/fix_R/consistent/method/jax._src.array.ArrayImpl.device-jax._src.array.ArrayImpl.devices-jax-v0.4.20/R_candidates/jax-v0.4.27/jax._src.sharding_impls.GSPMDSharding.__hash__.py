  def __hash__(self):
    if not hasattr(self, '_hash'):
      self._hash = hash((self._internal_device_list, self._hlo_sharding_hash,  # type: ignore
                        self.memory_kind))
    return self._hash
