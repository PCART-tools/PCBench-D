def to_gspmd_sharding(s: XLACompatibleSharding, ndim: int) -> GSPMDSharding:
  if isinstance(s, GSPMDSharding):
    return s
  gspmd_sharding = GSPMDSharding(
      s._device_assignment, s._to_xla_op_sharding(ndim))
  gspmd_sharding._original_sharding = s
  return gspmd_sharding
