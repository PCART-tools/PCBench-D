def _copy_impl(prim, *args, **kwargs):
  a, = args
  if isinstance(a, jax.Array) and isinstance(a.sharding, PmapSharding):
    sharded_dim = _which_dim_sharded(a.sharding)
    return _copy_impl_pmap_sharding(sharded_dim, *args, **kwargs)
  return xla.apply_primitive(prim, *args, **kwargs)
