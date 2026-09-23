def _op_sharding_to_numpy_indices(
    op_sharding: xc.OpSharding, shape: Sequence[int],
    num_devices: int) -> np.ndarray:
  indices = np.empty(num_devices, dtype=np.object_)

  # num_devices is required as an argument when op_sharding is
  # REPLICATED. `jax.device_count()` cannot be used because you can create
  # an opsharding with less number of devices than `jax.device_count()`.
  if is_op_sharding_replicated(op_sharding):
    indices.fill((slice(None),) * len(shape))
    return indices

  assert num_devices == len(op_sharding.tile_assignment_devices)

  partitions, num_replicas = get_num_ways_dim_sharded(op_sharding)
  assert len(partitions) == len(shape), (len(partitions), len(shape))

  axis_indices: List[Sequence[Index]] = []
  for dim, n_shards in zip(shape, partitions):
    if n_shards == 1:
      axis_indices.append([slice(None)])
    elif n_shards > 1:
      shard_size, ragged = divmod(dim, n_shards)
      assert not ragged, (dim, n_shards)
      axis_indices.append([slice(i * shard_size, (i + 1) * shard_size)
                           for i in range(n_shards)])
    else:
      raise AssertionError('Unrecognized number of shards. Please file a bug!')

  device_it = iter(op_sharding.tile_assignment_devices)
  for i, idxs in enumerate(it.product(*axis_indices)):
    for _ in range(num_replicas):
      indices[next(device_it)] = idxs
  return indices
