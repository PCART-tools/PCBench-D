def _get_op_sharding(op_sharding) -> Sequence[xc.OpSharding]:
  if op_sharding.type == xc.OpSharding.Type.TUPLE:
    out: List[xc.OpSharding] = []
    for s in op_sharding.tuple_shardings:
      out.extend(_get_op_sharding(s))
    return out
  else:
    return [op_sharding]
