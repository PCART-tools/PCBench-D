def get_logical_mesh_ids(mesh_shape):
  return np.arange(math.prod(mesh_shape)).reshape(mesh_shape)
