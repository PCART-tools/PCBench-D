def get_sharding_attr(sharding_proto: xc.OpSharding):
  if xc.mlir_api_version >= 44:
    return ir.StringAttr.get(repr(xc.HloSharding.from_proto(sharding_proto)))
  else:
    return ir.StringAttr.get(sharding_proto.SerializeToString())
