def new_mesh_sharding_specs(axis_sizes, axis_names):
  mesh_axis_pos = {name: i for i, name in enumerate(axis_names)}
  return partial(_make_sharding_spec, axis_sizes, mesh_axis_pos)
