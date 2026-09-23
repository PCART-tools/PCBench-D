def _check_sharding(x, s):
  if isinstance(s, Sharding):
    aval = shaped_abstractify(x)
    if isinstance(s, XLACompatibleSharding) and not isinstance(s, PmapSharding):
      pjit.pjit_check_aval_sharding(
          (s,), (aval,), None, "device_put args", allow_uneven_sharding=False)
    s.shard_shape(aval.shape)  # should raise an Error if incompatible
