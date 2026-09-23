def _put_x(x, s: Sharding, aval: core.AbstractValue, committed: bool):
  result_handler = pxla.global_aval_to_result_handler(aval, s, committed, False)
  map_ = s.devices_indices_map(aval.shape)  # type: ignore
  return result_handler(pxla.shard_arg(x, list(map_), list(map_.values()), s))
