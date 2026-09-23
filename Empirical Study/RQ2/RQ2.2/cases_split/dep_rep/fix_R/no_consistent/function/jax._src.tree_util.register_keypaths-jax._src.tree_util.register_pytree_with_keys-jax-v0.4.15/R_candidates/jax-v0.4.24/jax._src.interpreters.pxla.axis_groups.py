def axis_groups(axis_env: sharding_impls.AxisEnv, name) -> tuple[tuple[int, ...]]:
  if not isinstance(name, (list, tuple)):
    name = (name,)
  mesh_axes = tuple(unsafe_map(partial(_axis_read, axis_env), name))
  trailing_size, ragged = divmod(axis_env.nreps, math.prod(axis_env.sizes))
  assert not ragged
  mesh_spec = axis_env.sizes + (trailing_size,)
  return _axis_groups(mesh_spec, mesh_axes)
