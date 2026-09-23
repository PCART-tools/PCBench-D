  def shard_shape(self, global_shape: Shape) -> Shape:
    sharded_dim = None
    sharded_dim_size = None
    for i, s in enumerate(self.sharding_spec.sharding):
      if isinstance(s, sharding_specs.Unstacked):
        sharded_dim = i
        sharded_dim_size = s.size
        sharded_shape = util.tuple_delete(global_shape, sharded_dim)
        break
      elif isinstance(s, sharding_specs.Chunked):
        sharded_dim = i
        assert len(s.chunks) == 1, s.chunks
        sharded_dim_size = s.chunks[0]
        sharded_shape = util.tuple_update(global_shape, sharded_dim, 1)
        break
    if sharded_dim is None:
      return global_shape
    if global_shape[sharded_dim] != sharded_dim_size:
      raise ValueError(
          f'The sharded dimension must be equal to the number of '
          f'devices passed to PmapSharding. Got sharded dimension {sharded_dim} '
          f'with value {global_shape[sharded_dim]} in shape {global_shape} and '
          f'the number of devices={len(self._device_assignment)}')
    return sharded_shape
