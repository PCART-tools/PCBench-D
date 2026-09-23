def _pmap_sharding_spec(nrep, axis_size, npart, parts,
                        sharded_aval, map_axis: int | None) -> ShardingSpec:
  assert npart == 1, npart
  assert parts is None, parts
  return sharding_specs.pmap_sharding_spec(
      nrep, axis_size, sharded_aval.shape, map_axis)
