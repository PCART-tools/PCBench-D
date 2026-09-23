def _to_logical_sharding(
    aval: core.AbstractValue, sharding: MaybeSharding | AUTO
) -> sharding_impls.XLACompatibleSharding | None:
  if is_unspecified(sharding) or is_auto(sharding):
    return None
  elif isinstance(aval, (ShapedArray, DShapedArray)):
    assert isinstance(sharding, sharding_impls.XLACompatibleSharding)
    return sharding
  elif isinstance(aval, core.AbstractToken):
    return None
  else:
    raise TypeError(aval)
