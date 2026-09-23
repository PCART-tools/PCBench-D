def _check_sharding(aval, s):
  from jax._src import pjit

  if isinstance(s, XLACompatibleSharding) and not isinstance(s, PmapSharding):
    pjit.pjit_check_aval_sharding(
        (s,), (aval,), "device_put args", allow_uneven_sharding=False)

  s.shard_shape(aval.shape)  # should raise an Error if incompatible
