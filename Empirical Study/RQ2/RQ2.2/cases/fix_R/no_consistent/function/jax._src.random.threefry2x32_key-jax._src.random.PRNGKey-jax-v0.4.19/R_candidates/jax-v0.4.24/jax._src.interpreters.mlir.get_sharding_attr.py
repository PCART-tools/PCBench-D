def get_sharding_attr(sharding_proto: xc.OpSharding):
  # If there are very large numbers of devices, use the proto representation.
  # The MHLO to HLO conversion supports both, and the proto representation is
  # more compact.
  if len(sharding_proto.tile_assignment_devices) > 100:
    return ir.StringAttr.get(sharding_proto.SerializeToString())
  else:
    return ir.StringAttr.get(repr(xc.HloSharding.from_proto(sharding_proto)))
