def _sharding_spec_indices(self, shape: tuple[int, ...]) -> np.ndarray:
  """Returns NumPy-style indices corresponding to a sharding spec.

  Args:
    shape: The shape of the logical array being sharded.

  Returns:
    An ndarray with the same shape as the logical mesh (as derived form
    `mesh_mapping`). Each entry is a NumPy-style index selecting the subset of
    the data array to be placed on a corresponding device. The indices can be
    ints, slice objects with step=1, or tuples of those.
  """
  assert len(shape) == len(self.sharding), (shape, self.sharding)

  has_unstacked = any(isinstance(s, Unstacked) for s in self.sharding)
  # Take the op sharding indices generation route for pjit/xmap cases.
  if not has_unstacked:
    hlo_sharding = sharding_spec_sharding_proto(self)
    return op_shardings.op_sharding_to_numpy_indices(
        hlo_sharding, shape, math.prod(self.mesh_shape)
    ).reshape(self.mesh_shape)

  axis_indices: list[Sequence[Index]] = []
  shard_indices_shape = []
  for dim, sharding in enumerate(self.sharding):
    axis_size = shape[dim]
    if isinstance(sharding, NoSharding):
      axis_indices.append([slice(None)])
      # NOTE: We don't append unsharded dimensions to shard_indices_shape here,
      #       because they do not appear in the mesh mapping.
    elif isinstance(sharding, Unstacked):
      assert axis_size == sharding.size, f'{axis_size} != {sharding.size}'
      axis_indices.append(range(axis_size))
      shard_indices_shape.append(axis_size)
    elif isinstance(sharding, Chunked):
      total_chunks = math.prod(sharding.chunks)
      shard_size, ragged = divmod(axis_size, total_chunks)
      assert not ragged, (axis_size, total_chunks, dim)
      axis_indices.append([slice(i * shard_size, (i + 1) * shard_size)
                           for i in range(total_chunks)])
      shard_indices_shape.extend(sharding.chunks)
    else:
      util.assert_unreachable(sharding)

  # shard_indices is an ndarray representing the sharded axes of the logical array,
  # with each dimension having size equal to the number of shards across the corresponding
  # logical array dimension, and each element containing the multi-dimensional index that
  # is used to extract the corresponding shard of the logical array.
  shard_indices = np.empty([math.prod(shard_indices_shape)], dtype=np.object_)
  for i, idxs in enumerate(itertools.product(*axis_indices)):
    shard_indices[i] = idxs
  shard_indices = shard_indices.reshape(shard_indices_shape)

  # Ensure that each sharded axis is used exactly once in the mesh mapping
  num_sharded_dim = len(shard_indices_shape)
  sharded_dim_perm = [a.axis for a in self.mesh_mapping if isinstance(a, ShardedAxis)]
  assert (set(sharded_dim_perm) == set(range(num_sharded_dim)) and
          len(sharded_dim_perm) == num_sharded_dim)
  # Replicate/reorder the indices according to the mesh mapping
  replica_sizes = tuple(a.replicas for a in self.mesh_mapping if isinstance(a, Replicated))
  replica_dim, sharded_dim = itertools.count(0), iter(sharded_dim_perm)
  perm = [next(replica_dim) if isinstance(a, Replicated) else
          len(replica_sizes) + next(sharded_dim)
          for a in self.mesh_mapping]
  return (np.broadcast_to(shard_indices, replica_sizes + shard_indices.shape)
            .transpose(perm))
