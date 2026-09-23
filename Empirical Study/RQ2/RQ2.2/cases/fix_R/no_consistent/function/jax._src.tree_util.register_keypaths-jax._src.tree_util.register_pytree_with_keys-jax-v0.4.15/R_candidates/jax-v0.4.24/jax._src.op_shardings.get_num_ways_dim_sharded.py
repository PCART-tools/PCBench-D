def get_num_ways_dim_sharded(
    hlo_sharding: xc.HloSharding) -> tuple[Sequence[int], int]:
  if hlo_sharding.is_replicated():  # type: ignore
    return [], 1
  partitions = hlo_sharding.tile_assignment_dimensions()
  subgroup_types = hlo_sharding.subgroup_types()

  if subgroup_types == [xc.OpSharding.Type.REPLICATED]:
    replicate_on_last_tile_dim = True
  else:
    replicate_on_last_tile_dim = hlo_sharding.replicate_on_last_tile_dim()
    if subgroup_types:
      raise NotImplementedError(
          "Unhandled OpSharding type. Please open a bug report!")
  num_replicas = 1
  if replicate_on_last_tile_dim:
    num_replicas = partitions[-1]
    partitions = partitions[:-1]
  return partitions, num_replicas
