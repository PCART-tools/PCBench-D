@lru_cache(maxsize=2048)
def to_gspmd_sharding(s: XLACompatibleSharding, ndim: int,
                      device_or_backend_set: bool = False) -> GSPMDSharding:
  if isinstance(s, GSPMDSharding):
    return s
  gs = GSPMDSharding(s._device_assignment, s._to_xla_hlo_sharding(ndim),
                      memory_kind=s.memory_kind)
  gs._original_sharding = s
  if device_or_backend_set:
    gs._original_sharding._device_backend = device_or_backend_set
  return gs
