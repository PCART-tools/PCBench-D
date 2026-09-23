def _make_sharding_spec(axis_sizes, mesh_axis_pos, num_dimensions, aval_axes):
  mesh_mapping = [Replicated(axis_size) for axis_size in axis_sizes.values()]
  sharding = [_UNSHARDED_INSTANCE] * num_dimensions
  next_sharded_axis = 0
  # NOTE: sorted is stable, which is important when multiple resources
  #       map to the same axis.
  for name, axis in sorted(aval_axes.items(), key=lambda x: x[1]):
    chunked = sharding[axis]
    if isinstance(chunked, NoSharding):
      chunked = Chunked([])
    sharding[axis] = Chunked(list(chunked.chunks) + [axis_sizes[name]])
    assert isinstance(mesh_mapping[mesh_axis_pos[name]], Replicated), \
        "Value mapped to the same mesh axis twice"
    mesh_mapping[mesh_axis_pos[name]] = ShardedAxis(next_sharded_axis)
    next_sharded_axis += 1
  return ShardingSpec(sharding, mesh_mapping)
