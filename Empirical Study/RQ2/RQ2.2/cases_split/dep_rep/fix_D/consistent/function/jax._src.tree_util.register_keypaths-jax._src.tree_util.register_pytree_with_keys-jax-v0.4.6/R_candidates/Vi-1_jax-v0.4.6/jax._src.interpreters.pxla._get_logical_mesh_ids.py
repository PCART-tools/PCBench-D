def _get_logical_mesh_ids(mesh_shape):
  return np.arange(np.prod(mesh_shape)).reshape(mesh_shape)
