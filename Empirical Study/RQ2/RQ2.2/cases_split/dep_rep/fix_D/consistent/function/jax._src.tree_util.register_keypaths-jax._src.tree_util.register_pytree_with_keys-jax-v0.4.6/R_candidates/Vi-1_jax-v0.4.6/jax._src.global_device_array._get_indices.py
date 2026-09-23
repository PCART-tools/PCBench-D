def _get_indices(global_shape: Shape, global_mesh: pxla.Mesh,
                 mesh_axes: MeshAxes) -> Tuple[Index, ...]:
  sharding_spec = _get_sharding_spec(global_shape, global_mesh, mesh_axes)
  indices = pxla.spec_to_indices(global_shape, sharding_spec)
  return indices  # type: ignore
