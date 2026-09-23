def pmap_sharding_spec(nrep, axis_size, sharded_shape: Sequence[int],
                       map_axis: int | None) -> ShardingSpec:
  """Sharding spec for arguments or results of a pmap.
  Args:
    nrep: number of local XLA replicas (product of local axis sizes)
    axis_size: local axis size for outer pmap
    sharded_aval: the aval of the value inside the outer pmap, an instance of
      a ShapedArray.
    map_axis: the axis along which the value is mapped in the outer pmap
  Returns:
    A ShardingSpec.
  """
  replication_factor, ragged = divmod(nrep, axis_size)
  assert not ragged
  pspec = ShardingSpec(sharding=[_UNSHARDED_INSTANCE] * len(sharded_shape),
                       mesh_mapping=())
  maybe_replicate = () if replication_factor == 1 else (Replicated(replication_factor),)
  if map_axis is not None:
    sharded_in_axis = sum(not isinstance(s, NoSharding) for s in pspec.sharding[:map_axis])
    def shift_sharded_axis(a: MeshDimAssignment):
      if isinstance(a, ShardedAxis) and a.axis >= sharded_in_axis:
        return ShardedAxis(a.axis + 1)
      return a
    # replication_factor represents the product of inner pmaps, so it goes
    # after the outer pmapped axis at index 0
    if config.pmap_no_rank_reduction.value:
      sharding = util.tuple_update(
          pspec.sharding, map_axis, Chunked([axis_size]))
    else:
      sharding = util.tuple_insert(
          pspec.sharding, map_axis, Unstacked(axis_size))
    return ShardingSpec(
      sharding=sharding,
      mesh_mapping=itertools.chain(
          [ShardedAxis(sharded_in_axis)], maybe_replicate,
          map(shift_sharded_axis, pspec.mesh_mapping)))
  else:
    return ShardingSpec(
      sharding=pspec.sharding,
      mesh_mapping=(Replicated(axis_size),) + maybe_replicate + pspec.mesh_mapping)
