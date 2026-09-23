def _pmap_sharding_spec(nrep, axis_size, npart, parts, sharded_aval,
                        map_axis: Optional[int]) -> ShardingSpec:
  """Sharding spec for arguments or results of a pmap.
  Args:
    nrep: number of local XLA replicas (product of local axis sizes)
    axis_size: local axis size for outer pmap
    npart: total number of XLA partitions (required by sharded_jit calls)
    parts: the partitioning of the value or None
    sharded_aval: the aval of the value inside the outer pmap, an instance of
      a ShapedArray.
    map_axis: the axis along which the value is mapped in the outer pmap
  Returns:
    A ShardingSpec.
  """
  assert isinstance(sharded_aval, ShapedArray), sharded_aval
  replication_factor, ragged = divmod(nrep, axis_size)
  assert not ragged
  # get the sharding spec from inner sharded_jits as if we weren't in a pmap
  pspec = partitioned_sharding_spec(npart, parts, sharded_aval)
  maybe_replicate = () if replication_factor == 1 else (Replicated(replication_factor),)
  if map_axis is not None:
    sharded_in_axis = sum(not isinstance(s, NoSharding) for s in pspec.sharding[:map_axis])
    def shift_sharded_axis(a: MeshDimAssignment):
      if isinstance(a, ShardedAxis) and a.axis >= sharded_in_axis:
        return ShardedAxis(a.axis + 1)
      return a
    # replication_factor represents the product of inner pmaps, so it goes
    # after the outer pmapped axis at index 0
    return ShardingSpec(
      sharding=tuple_insert(pspec.sharding, map_axis, Unstacked(axis_size)),
      mesh_mapping=it.chain([ShardedAxis(sharded_in_axis)],
                            maybe_replicate,
                            map(shift_sharded_axis, pspec.mesh_mapping)))
  else:
    return ShardingSpec(
      sharding=pspec.sharding,
      mesh_mapping=(Replicated(axis_size),) + maybe_replicate + pspec.mesh_mapping)
