def get_sharding_attr(sharding_proto: xc.OpSharding):
  return ir.StringAttr.get(repr(xc.HloSharding.from_proto(sharding_proto)))
