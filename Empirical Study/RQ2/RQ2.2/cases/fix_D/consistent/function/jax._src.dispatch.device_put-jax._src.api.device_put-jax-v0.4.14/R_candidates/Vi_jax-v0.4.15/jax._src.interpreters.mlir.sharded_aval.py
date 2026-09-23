def sharded_aval(aval: core.AbstractValue,
                 sharding: XLACompatibleSharding | None) -> core.AbstractValue:
  """Returns the new aval sharded based on sharding proto."""
  if sharding is None:
    return aval
  if isinstance(aval, core.AbstractToken):
    return aval
  if not isinstance(aval, (core.ShapedArray, core.DShapedArray)):
    raise NotImplementedError
  return aval.update(sharding.shard_shape(aval.shape))
