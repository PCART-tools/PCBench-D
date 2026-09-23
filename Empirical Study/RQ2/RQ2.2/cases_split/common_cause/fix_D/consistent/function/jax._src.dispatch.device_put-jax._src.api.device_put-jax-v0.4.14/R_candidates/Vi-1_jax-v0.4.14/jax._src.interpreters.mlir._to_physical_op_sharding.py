def _to_physical_op_sharding(
    aval: core.AbstractValue | None, sharding: xc.HloSharding | None
) -> xc.OpSharding | None:
  if (isinstance(aval, core.ShapedArray) and dtypes.issubdtype(aval.dtype, dtypes.extended)
      and sharding is not None):
    return aval.dtype._rules.physical_hlo_sharding(aval, sharding).to_proto()
  return None if sharding is None else sharding.to_proto()  # type: ignore
