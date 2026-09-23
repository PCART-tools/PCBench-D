def _copy_impl(prim, *args, **kwargs):
  a, = args
  if isinstance(a, jax.Array) and isinstance(a.sharding, PmapSharding):
    sharded_dim = _which_dim_sharded(a.sharding)
    if sharded_dim is None:
      return dispatch.apply_primitive(prim, *args, **kwargs)
    return _copy_impl_pmap_sharding(sharded_dim, *args, **kwargs)
  return dispatch.apply_primitive(prim, *args, **kwargs)
