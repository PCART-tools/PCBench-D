def _create_pmap_sharding_spec(aval, sharded_dim=0, sharded_dim_size=None):
  return sharding_specs.create_pmap_sharding_spec(
      aval.shape, sharded_dim, sharded_dim_size)
