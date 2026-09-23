  def with_memory_kind(self, kind: str) -> GSPMDSharding:
    return GSPMDSharding(self._devices, self._hlo_sharding, memory_kind=kind)
