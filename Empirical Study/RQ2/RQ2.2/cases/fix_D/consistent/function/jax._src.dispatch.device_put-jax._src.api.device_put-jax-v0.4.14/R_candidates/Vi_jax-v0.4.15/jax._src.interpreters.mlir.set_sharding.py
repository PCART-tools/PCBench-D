def set_sharding(op, sharding_proto: xc.OpSharding):
  op.attributes["mhlo.sharding"] = get_sharding_attr(sharding_proto)
