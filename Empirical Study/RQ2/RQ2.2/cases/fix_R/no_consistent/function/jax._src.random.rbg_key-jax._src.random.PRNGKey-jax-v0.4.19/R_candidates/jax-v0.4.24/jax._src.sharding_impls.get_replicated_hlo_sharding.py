@functools.lru_cache
def get_replicated_hlo_sharding():
  return xc.HloSharding.replicate()
