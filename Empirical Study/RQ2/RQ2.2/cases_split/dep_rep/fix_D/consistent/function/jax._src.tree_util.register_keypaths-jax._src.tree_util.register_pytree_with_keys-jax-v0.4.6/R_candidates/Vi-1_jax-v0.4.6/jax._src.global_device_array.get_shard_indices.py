@functools.lru_cache(maxsize=4096)
def get_shard_indices(global_shape: Shape, global_mesh: pxla.Mesh,
                      mesh_axes: MeshAxes) -> Mapping[Device, Index]:
  indices = _get_indices(global_shape, global_mesh, mesh_axes)
  # The type: ignore is to ignore the type returned by `spec_to_indices`.
  return {
      d: i
      for d, i in safe_zip(global_mesh.devices.flat, indices)}  # type: ignore
