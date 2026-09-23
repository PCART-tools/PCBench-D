def _get_shard_indices_replica_ids_uncached(
    global_shape: Shape, global_mesh: pxla.Mesh,
    mesh_axes: MeshAxes) -> Mapping[Device, Tuple[Index, int]]:
  indices = _get_indices(global_shape, global_mesh, mesh_axes)
  index_to_replica: Dict[int, int] = Counter()
  out = {}
  unique_shards = 0
  for device, index in safe_zip(global_mesh.devices.flat, indices):
    h_index = _hashed_index(index)
    replica_id = index_to_replica[h_index]
    if replica_id == 0:
      unique_shards += 1
    index_to_replica[h_index] += 1
    out[device] = (index, replica_id)

  shard_shape = get_shard_shape(global_shape, global_mesh, mesh_axes)
  expected_unique_shards = math.prod(
      [g // s for g, s in safe_zip(global_shape, shard_shape) if g != 0 or s != 0])
  if expected_unique_shards != unique_shards:
    raise RuntimeError(
        f'Number of expected unique shards are: {expected_unique_shards} but '
        f'got {unique_shards}. Please file a bug at '
        'https://github.com/google/jax/issues.')
  return out
