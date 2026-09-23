def sharding_spec_sharding_proto(self, special_axes: Mapping[int, OpShardingType] = {}):
  """Converts a ShardingSpec to an OpSharding proto.

  See
  https://github.com/tensorflow/tensorflow/blob/master/tensorflow/compiler/xla/xla_data.proto#L601
  for details on the OpSharding proto.
  Unfortunately the semantics are not very well described in the proto spec, but the code here might help:
  https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/compiler/xla/experimental/xla_sharding/xla_sharding.py
  """
  mesh_shape = cast(Tuple[int, ...], self.mesh_shape)
  mesh = _get_logical_mesh_ids(self.mesh_shape)

  sharded_axes = {}  # maps sharded axis identifiers to mesh axis indices to which they're mapped
  replicated_maxes = []  # lists mesh axis identifiers to replicate over
  for maxis, assignment in enumerate(self.mesh_mapping):
    if isinstance(assignment, Replicated):
      replicated_maxes.append((maxis, assignment.replicas))
    elif isinstance(assignment, ShardedAxis):
      sharded_axes[assignment.axis] = maxis
    else:
      assert_unreachable(assignment)

  proto = xc.OpSharding()
  if len(replicated_maxes) == len(self.mesh_mapping) and not special_axes:
    proto.type = xc.OpSharding.Type.REPLICATED
    return proto
  else:
    proto.type = xc.OpSharding.Type.OTHER

  mesh_permutation = []
  new_mesh_shape = []
  next_sharded_axis = 0
  for axis, sharding in enumerate(self.sharding):
    if isinstance(sharding, NoSharding):
      new_mesh_shape.append(1)  # Add a dummy mesh axis we won't be sharding over
    elif isinstance(sharding, Chunked):
      for nchunks in sharding.chunks:
        maxis = sharded_axes[next_sharded_axis]
        assert mesh_shape[maxis] == nchunks
        mesh_permutation.append(maxis)
        next_sharded_axis += 1
      new_mesh_shape.append(int(np.prod(sharding.chunks)))
    elif isinstance(sharding, Unstacked):
      raise RuntimeError("Cannot convert unstacked sharding specs to XLA OpSharding")
    else:
      assert_unreachable(sharding)

  # Create a partial sharding proto if tensor is replicated or partitioned
  # specially over some mesh axes.
  if replicated_maxes:
    last_tile_dims = []
    axes_by_type: Dict[OpShardingType, List[MeshAxisName]] = {}
    size_by_type: Dict[OpShardingType, int] = defaultdict(lambda: 1)
    assert {x[0] for x in replicated_maxes}.issuperset(set(special_axes.keys()))
    for axis, size in replicated_maxes:
      ty = special_axes.get(axis, xc.OpSharding.Type.REPLICATED)
      axes_by_type.setdefault(ty, []).append(axis)
      size_by_type[ty] *= size
    for ty, axes in sorted(axes_by_type.items(), key=lambda x: x[0].value):
      last_tile_dims.append(ty)
      new_mesh_shape.append(size_by_type[ty])
      mesh_permutation.extend(axes)
    proto.last_tile_dims = last_tile_dims

  proto_mesh = mesh.transpose(mesh_permutation).reshape(new_mesh_shape)
  proto.tile_assignment_dimensions = list(proto_mesh.shape)
  proto.tile_assignment_devices = list(proto_mesh.flat)
  return proto
