  def __reduce__(self):
    return (type(self), (self._devices, self._hlo_sharding.to_proto()),
            {'memory_kind': self._memory_kind})
