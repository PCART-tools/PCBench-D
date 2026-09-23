def get_num_ways_dim_sharded(op_sharding: xc.OpSharding) -> Tuple[Sequence[int], int]:
  partitions = op_sharding.tile_assignment_dimensions
  if op_sharding.last_tile_dims == [xc.OpSharding.Type.REPLICATED]:
    replicate_on_last_tile_dim = True
  else:
    replicate_on_last_tile_dim = op_sharding.replicate_on_last_tile_dim
    if op_sharding.last_tile_dims:
      raise NotImplementedError("Unhandled OpSharding type. Please open a bug report!")
  num_replicas = 1
  if replicate_on_last_tile_dim:
    num_replicas = partitions[-1]
    partitions = partitions[:-1]
  return partitions, num_replicas
