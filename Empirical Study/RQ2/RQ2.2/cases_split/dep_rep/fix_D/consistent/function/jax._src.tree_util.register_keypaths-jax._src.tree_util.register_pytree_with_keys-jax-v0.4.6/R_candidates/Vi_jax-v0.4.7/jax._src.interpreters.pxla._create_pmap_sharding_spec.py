def _create_pmap_sharding_spec(aval, sharded_dim=0, sharded_dim_size=None):
  if sharded_dim is not None:
    sharded_aval = aval.update(
        shape=aval.shape[:sharded_dim] + aval.shape[sharded_dim+1:])
    if sharded_dim_size is None:
      sharded_dim_size = aval.shape[sharded_dim]
  else:
    assert sharded_dim_size is not None
    sharded_aval = aval

  return _pmap_sharding_spec(sharded_dim_size, sharded_dim_size, 1, None,
                             sharded_aval, sharded_dim)
