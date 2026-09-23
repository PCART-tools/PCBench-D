def create_global_mesh(mesh_shape, axis_names):
  size = prod(mesh_shape)
  if len(api.devices()) < size:
    raise unittest.SkipTest(f"Test requires {size} global devices.")
  devices = sorted(api.devices(), key=lambda d: d.id)
  mesh_devices = np.array(devices[:size]).reshape(mesh_shape)
  global_mesh = Mesh(mesh_devices, axis_names)
  return global_mesh
