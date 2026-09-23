  def __hash__(self):
    if not hasattr(self, '_hash'):
      self._hash = hash((self._internal_device_list, self.sharding_spec))  # type: ignore
    return self._hash
