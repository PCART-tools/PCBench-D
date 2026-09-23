@functools.lru_cache(maxsize=4096)
def get_shard_indices_replica_ids(
    global_shape: Shape, global_mesh: pxla.Mesh,
    mesh_axes: MeshAxes) -> Mapping[Device, Tuple[Index, int]]:
  return _get_shard_indices_replica_ids_uncached(global_shape, global_mesh, mesh_axes)
