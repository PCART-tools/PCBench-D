@functools.lru_cache()
def get_replicated_op_sharding():
  proto = xc.OpSharding()
  proto.type = xc.OpSharding.Type.REPLICATED
  return proto
