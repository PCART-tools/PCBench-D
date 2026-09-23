@contextmanager
def with_mesh(named_shape: MeshSpec) -> Generator[None, None, None]:
  """Test utility for setting up meshes given mesh data from `schedules`."""
  # This is similar to the `with_mesh` function above, but isn't a decorator.
  axis_names, shape = unzip2(named_shape)
  size = math.prod(shape)
  local_devices = list(jax.local_devices())
  if len(local_devices) < size:
    raise unittest.SkipTest(f"Test requires {size} local devices")
  mesh_devices = np.array(local_devices[:size]).reshape(shape)  # type: ignore
  with jax.sharding.Mesh(mesh_devices, axis_names):
    yield
