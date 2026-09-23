def are_op_shardings_equal(op1: Union[xc.OpSharding, xc.HloSharding],
                           op2: Union[xc.OpSharding, xc.HloSharding]) -> bool:
  if id(op1) == id(op2):
    return True
  if is_op_sharding_replicated(op1) and is_op_sharding_replicated(op2):
    return True
  hc1 = xc.HloSharding.from_proto(op1) if isinstance(op1, xc.OpSharding) else op1
  hc2 = xc.HloSharding.from_proto(op2) if isinstance(op2, xc.OpSharding) else op2
  return hc1 == hc2
