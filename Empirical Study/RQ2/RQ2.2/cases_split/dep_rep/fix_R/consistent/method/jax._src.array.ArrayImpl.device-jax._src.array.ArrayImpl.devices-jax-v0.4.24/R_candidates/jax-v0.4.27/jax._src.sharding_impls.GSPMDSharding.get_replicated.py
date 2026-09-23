  @classmethod
  def get_replicated(cls, device_assignment, *, memory_kind: str | None = None):
    return cls(tuple(device_assignment), get_replicated_hlo_sharding(),
               memory_kind=memory_kind)
