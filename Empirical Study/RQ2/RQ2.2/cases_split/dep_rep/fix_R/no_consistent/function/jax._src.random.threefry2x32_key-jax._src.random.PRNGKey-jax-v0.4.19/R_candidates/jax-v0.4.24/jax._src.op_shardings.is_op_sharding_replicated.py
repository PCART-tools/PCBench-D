def is_op_sharding_replicated(op: xc.OpSharding | xc.HloSharding) -> bool:
  if isinstance(op, xc.OpSharding):
    op = xc.HloSharding.from_proto(op)
  if op.num_devices() == 1:
    return True
  return op.is_replicated()  # type: ignore
