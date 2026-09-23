def _which_dim_sharded(s: PmapSharding) -> Optional[int]:
  sharded_dim = None
  for i, s in enumerate(s.sharding_spec.sharding):
    if isinstance(s, pxla.Unstacked):
      sharded_dim = i
      break
  return sharded_dim
