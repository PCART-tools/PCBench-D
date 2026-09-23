def is_op_sharding_replicated(op: xc.OpSharding) -> bool:
  if len(op.tile_assignment_devices) == 1:
    return True
  return xc.HloSharding.from_proto(op).is_replicated()  # type: ignore
