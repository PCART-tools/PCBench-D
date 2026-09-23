def are_op_shardings_equal(op1: xc.OpSharding, op2: xc.OpSharding) -> bool:
  if id(op1) == id(op2):
    return True
  if is_op_sharding_replicated(op1) and is_op_sharding_replicated(op2):
    return True
  return xc.HloSharding.from_proto(op1) == xc.HloSharding.from_proto(op2)
