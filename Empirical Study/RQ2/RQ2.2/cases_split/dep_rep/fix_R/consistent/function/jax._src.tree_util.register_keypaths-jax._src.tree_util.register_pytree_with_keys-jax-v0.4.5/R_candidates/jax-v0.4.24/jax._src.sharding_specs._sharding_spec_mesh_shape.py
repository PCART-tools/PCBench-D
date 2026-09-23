def _sharding_spec_mesh_shape(self):
  sharded_axis_sizes = []
  for sharding in self.sharding:
    if isinstance(sharding, NoSharding):
      continue
    elif isinstance(sharding, Unstacked):
      sharded_axis_sizes.append(sharding.size)
    elif isinstance(sharding, Chunked):
      sharded_axis_sizes.extend(sharding.chunks)
    else:
      util.assert_unreachable(sharding)
  return tuple(sharded_axis_sizes[a.axis] if isinstance(a, ShardedAxis)
               else a.replicas
               for a in self.mesh_mapping)
