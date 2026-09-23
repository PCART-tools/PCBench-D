def _to_logical_op_sharding(
    aval: core.AbstractValue, sharding: XLACompatibleSharding | None,
) -> xc.HloSharding | None:
  if sharding is None:
    return None
  assert isinstance(sharding, sharding_impls.XLACompatibleSharding)
  assert isinstance(aval, (core.ShapedArray, core.DShapedArray))
  return sharding._to_xla_hlo_sharding(aval.ndim)
