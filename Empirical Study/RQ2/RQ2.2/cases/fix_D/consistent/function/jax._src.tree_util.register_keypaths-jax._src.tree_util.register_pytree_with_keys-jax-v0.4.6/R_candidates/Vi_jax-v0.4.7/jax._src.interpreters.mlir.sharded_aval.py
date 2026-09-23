def sharded_aval(aval: core.ShapedArray,
                 sharding: Optional[xc.OpSharding]) -> core.ShapedArray:
  """Returns the new aval sharded based on sharding proto."""
  if sharding is None:
    return aval

  if (sharding.type == xc.OpSharding.Type.REPLICATED or
      sharding.type == xc.OpSharding.Type.MANUAL):
    return aval

  sharded_shape = []
  tile_rank = len(sharding.tile_assignment_dimensions)
  if sharding.replicate_on_last_tile_dim:
    tile_rank -= 1
  if sharding.last_tile_dims:
    tile_rank -= len(sharding.last_tile_dims)
  if tile_rank == 0:
    return aval

  for i in range(tile_rank):
    partitions = sharding.tile_assignment_dimensions[i]
    assert partitions > 0
    sharded_shape.append((aval.shape[i] + partitions - 1) // partitions)
  return aval.update(tuple(sharded_shape))
