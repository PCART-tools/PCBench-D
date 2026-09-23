def _get_sharding_spec(global_shape, global_mesh, mesh_axes):
  array_mapping = pxla.get_array_mapping(mesh_axes)
  # The dtype doesn't matter for creating sharding specs.
  aval = core.ShapedArray(global_shape, np.float32)
  return pxla.mesh_sharding_specs(global_mesh.shape,
                                  global_mesh.axis_names)(aval, array_mapping)
